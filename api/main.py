import os
import json
import numpy as np
import redis
import hashlib
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Request
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from traditional_rag.rag import get_or_create_index

# Load env
load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="RAG Service API")

# Redis setup
redis_client = redis.Redis(host="redis",port=6379,decode_responses=True)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request,exc):
    return JSONResponse(
        status_code=429,
        content={"error":"Rate limit exceeded"}
    )

def generate_cache_key(prefix:str,query:str):
    return f"{prefix}:{hashlib.md5(query.encode()).hexdigest()}"

index,chunks = get_or_create_index()
# ------------------------
# Request schema
# ------------------------

class QueryRequest(BaseModel):
    query:str

# --------------------
# Load Data
# --------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Graph RAG Setup --
with open(os.path.join(BASE_DIR,"data","graph.json"),"r") as f:
    graph = json.load(f)

# ----- Health Check -----
@app.get("/health")
def health():
    return {"status":"RAG Service API is Running!!"}

# ---- Traditional RAG Endpoint -----
@app.post("/traditional-rag")
@limiter.limit("5/minute")
async def traditional_rag(request:Request,body:QueryRequest):
    query = body.query
    cache_key = generate_cache_key("trad",query)
    
    # Check cache
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)
    
    # Embed query
    q_emb = await client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )

    q_emb = np.array([q_emb.data[0].embedding],dtype="float32")

    # FAISS Search (sync)
    _,indices = index.search(q_emb,3)
    retrieved_chunks = [chunks[i]for i in indices[0]]
    context = "\n\n".join(retrieved_chunks)

    # LLM response (async)
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input = [
            {
                "role":"system",
                "content":"Answer strictly based on the provided context."

            },
            {
                "role":"user",
                "content":f"Context:\n{context}\n\nQuestion: {query}"
            }
        ],
        temperature=0
    )
    answer= response.output[0].content[0].text

    result = {
        "query":query,
        "retrieved_chunks":retrieved_chunks,
        "answer":answer
    }

    # Store in cache(TTL= 5 min)
    redis_client.setex(cache_key,300,json.dumps(result))
    return result

# ---- GRAPH RAG Endpoint --------

@app.post("/graph-rag")
@limiter.limit("5/minute")
async def graph_rag(request: Request,body:QueryRequest):
    query=body.query

    cache_key = generate_cache_key("graph",query)
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)
    
    # Entity extraction
    extracted_entities = [
        node["id"]
        for node in graph["nodes"]
        if node["id"].lower() in query.lower()
    ]
    # Validate edges
    valid_edges =[
        e for e in graph["edges"]
        if isinstance(e,dict)
        and "source" in e
        and "target" in e
        and "relation" in e
    ]

    # One hop
    relevant_edges= [
        e for e in valid_edges
        if e["source"] in extracted_entities or e["target"] in extracted_entities
    ]
    # Two-hop expansion
    connected_entities =set()
    for edge in relevant_edges:
        connected_entities.add(edge["source"])
        connected_entities.add(edge["target"])
    
    expanded_edges = [
        e for e in valid_edges
        if e["source"] in connected_entities or e["target"] in connected_entities
    ]

    # Deduplicate
    unique_edges={
        f"{e['source']}-{e['relation']}-{e['target']}":e
        for e in expanded_edges
    }.values()

    # Build context
    context = "Social Connections & Secrets:\n"
    for edge in unique_edges:
        context += f"- {edge['source']} {edge['relation']} {edge['target']}\n"
    
    # LLM response
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input = [
            {
                "role":"system",
                "content":"Answer strictly based on the provided relationships."
            },
            {
                "role":"user",
                "content":f"Context:\n{context}\n\nQuestion: {query}"
            }
        ],
        temperature=0
    )
    answer = response.output[0].content[0].text

    result = {
        "query":query,
        "entities":extracted_entities,
        "relationships":list(unique_edges),
        "answer":answer
    }
    redis_client.setex(cache_key,300,json.dumps(result))
    return result

# ------ Hybrid search RAG Endpoint------
@app.post("/hybrid-rag")
@limiter.limit("5/minute")
async def hybrid_rag(request: Request,body:QueryRequest):
    query= body.query

    cache_key = generate_cache_key("hybrid",query)
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    # ---- Vector RAG (FAISS) ---
    q_emb = await client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    q_emb = np.array([q_emb.data[0].embedding],dtype="float32")
    _,indices = index.search(q_emb,3)
    retrieved_chunks = [chunks[i]for i in indices[0]]

    vector_context= "\n\n".join(retrieved_chunks)

    # ----- GRAPH RAG -----
    extracted_entities = [
        node["id"]
        for node in graph["nodes"]
        if node["id"].lower() in query.lower()
    ]
    valid_edges = [
        e for e in graph["edges"]
        if isinstance(e,dict)
        and "source" in e
        and "target" in e
        and "relation" in e
    ]
    relevant_edges = [
        e for e in valid_edges
        if e["source"] in extracted_entities or e["target"] in extracted_entities
    ]

    connected_entities= set()
    for edge in relevant_edges:
        connected_entities.add(edge["source"])
        connected_entities.add(edge["target"])

    expanded_edges=[
        e for e in valid_edges 
        if e["source"] in connected_entities or e["target"] in connected_entities 
    ]
    unique_edges = {
        f"{e['source']}-{e['relation']}-{e['target']}":e
        for e in expanded_edges
    }.values()

    graph_context = "Graph Relationships:\n"
    for edge in unique_edges:
        graph_context +=f"- {edge['source']} {edge['relation']} {edge['target']}\n"

    # ---- MERGED CONTEXT -----
    final_context=f"""
    Vector Context:
    {vector_context}

    Graph Context:
    {graph_context}
"""
    # ----- LLM -----
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input = [
            {
                "role":"system",
                "content": """ Answer using BOTH:
                1. Vector context (text evidence)
                2. Graph relationships (connections)

                Prefer graph relationships for reasoning.
            """
            },
            {
                "role":"user",
                "content":f"Context:\n{final_context}\n\nQuestion: {query}"
            }
        ],
        temperature=0
    )
    answer = response.output[0].content[0].text

    result= {
        "query": query,
        "vector_chunks": retrieved_chunks,
        "graph_relationships": list(unique_edges),
        "answer": answer
    }

    redis_client.setex(cache_key,300,json.dumps(result))
    return result

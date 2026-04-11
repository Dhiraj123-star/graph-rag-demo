import os
import json
import faiss
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from traditional_rag.rag import get_or_create_index

# Load env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="RAG Service API")

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
    return {"status":"OK"}

# ---- Traditional RAG Endpoint -----
@app.post("/traditional-rag")
def traditional_rag(request:QueryRequest):
    query = request.query

    # Embed query
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )

    q_emb = np.array([q_emb.data[0].embedding],dtype="float32")

    # Search
    _,indices = index.search(q_emb,3)
    retrieved_chunks = [chunks[i]for i in indices[0]]
    context = "\n\n".join(retrieved_chunks)

    # LLM response
    response = client.responses.create(
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

    return {
        "query":query,
        "retrieved_chunks":retrieved_chunks,
        "answer":answer
    }

# ---- GRAPH RAG Endpoint --------

@app.post("/graph-rag")
def graph_rag(request:QueryRequest):
    query=request.query

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
    response = client.responses.create(
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

    return {
        "query":query,
        "entities":extracted_entities,
        "relationships":list(unique_edges),
        "answer":answer
    }

# ------ Hybrid search RAG Endpoint------
@app.post("/hybrid-rag")
def hybrid_rag(request:QueryRequest):
    query= request.query

    # ---- Vector RAG (FAISS) ---
    q_emb = client.embeddings.create(
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
    response = client.responses.create(
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

    return {
        "query": query,
        "vector_chunks": retrieved_chunks,
        "graph_relationships": list(unique_edges),
        "answer": answer
    }

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not set in .env")

client= OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "graph.json")


# 2. Load the Graph
with open(file_path, "r") as f:
    graph = json.load(f)

# 3. Query (Bridgerton universe)
query = "Who is the Lady in Silver and how is she connected to Lord Penwood?"

# 4. Entity Matching
# Match node names directly from the query
extracted_entities = [
    node["id"]
    for node in graph["nodes"]
    if node["id"].lower() in query.lower()
]

# 5. Retrieve Relevant Edges (One-hop)
relevant_edges = [
    e for e in graph["edges"]
    if e["source"] in extracted_entities or e["target"] in extracted_entities
]

# 6. Expand to Two-Hop (important for reasoning)
connected_entities = set()
for edge in relevant_edges:
    connected_entities.add(edge["source"])
    connected_entities.add(edge["target"])

expanded_edges = [
    e for e in graph["edges"]
    if e["source"] in connected_entities or e["target"] in connected_entities
]

# Remove duplicates
unique_edges = {
    f"{e['source']}-{e['relation']}-{e['target']}": e
    for e in expanded_edges
}.values()

# 7. Serialize relationships
context = "Social Connections & Secrets:\n"
for edge in unique_edges:
    context += f"- {edge['source']} {edge['relation']} {edge['target']}\n"

# 8. Generate Answer using OpenAI Responses API
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
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
# Extract text input
answer = response.output[0].content[0].text

# Print results
print("=== GRAPH RAG ===\n")
print("Entities Identified:", extracted_entities)
print("\nRetrieved Relationships:\n")
print(context)
print("Final Answer:\n")
print(answer)
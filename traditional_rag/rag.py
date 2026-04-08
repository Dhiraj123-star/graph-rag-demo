import os
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in .env")

client = OpenAI(api_key=api_key)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "documents.txt")

# 2. Load documents
with open(file_path, "r") as f:
    text = f.read()

# Split by single newline (since each document is one line)
chunks = [line.strip() for line in text.split("\n") if line.strip()]


# 3. Create Embeddings using OpenAI
embedding_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)

embeddings = [item.embedding for item in embedding_response.data]
embeddings= np.array(embeddings,dtype="float32")

# 4. Stored in FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 5. Query
query = "Who was the Lady in Silver and how is she connected to the Penwood family?"

query_embedding_response = client.embeddings.create(
    model= "text-embedding-3-small",
    input=[query]
)

q_emb = np.array([query_embedding_response.data[0].embedding],dtype="float32")

# 6. Retrieve Top-3
_, indices = index.search(q_emb, 3)
retrieved_chunks = [chunks[i] for i in indices[0]]
retrieved = "\n\n".join(retrieved_chunks)

# 7. Generate with OpenAI 
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role":"system",
            "content":"Answer strictly based on the provided context."

        },
        {
            "role" : "user",
            "content": f"Context:\n{retrieved}\n\nQuestion: {query}"
        }
    ],
    temperature=0
)

answer = response.output[0].content[0].text

# 8. Output
print("=== TRADITIONAL RAG(OPENAI Embeddings) ===")

print("\nRetrieved chunks:")
for chunk in retrieved_chunks:
    print("-", chunk)

print("\nAnswer:")
print(answer)
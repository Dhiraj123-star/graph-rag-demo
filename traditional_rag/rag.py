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

INDEX_PATH = os.path.join(BASE_DIR,"data","faiss.index")
EMBEDDINGS_PATH =  os.path.join(BASE_DIR,"data","embeddings.npy")
DOC_PATH = os.path.join(BASE_DIR,"data","documents.txt")

# 2. Load documents
def load_documents():
    with open(DOC_PATH,"r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# 3. Create Embeddings using OpenAI
def create_embeddings(chunks):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )
    return np.array([e.embedding for e in response.data]).astype("float32")


# 4. Stored in FAISS
def build_and_save_index(chunks):
    print("Creating embeddings and FAISS index ....")

    embeddings = create_embeddings(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save
    faiss.write_index(index,INDEX_PATH)
    np.save(EMBEDDINGS_PATH,embeddings)

    print("Index and embeddings saved")

    return index,embeddings


def load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(EMBEDDINGS_PATH) :
        print("Loading FAISS index from disk.....")
        index = faiss.read_index(INDEX_PATH)
        embeddings = np.load(EMBEDDINGS_PATH)
        return index,embeddings

    return None,None

def get_or_create_index():
    chunks = load_documents()
    index,embeddings = load_index()

    if index is None:
        index,embeddings = build_and_save_index(chunks)
    
    return index,chunks
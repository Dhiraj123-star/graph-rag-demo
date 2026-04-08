# Graph RAG vs Traditional RAG Demo

Minimal comparison of **Traditional RAG** and **Graph RAG** using the Bridgerton "Lady in Silver" mystery — now upgraded to use **OpenAI APIs (Embeddings + LLM)** and exposed via a **FastAPI service**.

---

## ❓ Question

Who is the Lady in Silver and how is she connected to Lord Penwood?

---

## 🎯 Purpose

Both systems use the same facts but different representations:

### **Traditional RAG**

* Stores text chunks
* Retrieves using vector similarity (FAISS)
* Uses **OpenAI embeddings** for semantic search

### **Graph RAG**

* Stores entities and relationships
* Retrieves using graph traversal (multi-hop reasoning)
* Uses **OpenAI LLM for reasoning**

---

## 🧰 Tech Stack

* **LLM**: OpenAI (`gpt-4.1-mini`)
* **Embeddings**: OpenAI (`text-embedding-3-small`)
* **Vector Search**: FAISS
* **Graph Storage**: JSON
* **API Layer**: FastAPI
* **Environment**: uv / venv
* **Config Management**: python-dotenv (.env)

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Make sure `.env` is added to `.gitignore`

---

## ⚙️ Setup

From the project root:

```bash
cd graph-rag-bridgerton-demo
```

Create and activate environment:

```bash
uv venv
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

---

## ▶️ Run

### **Run Scripts (Standalone)**

```bash
python traditional_rag/rag.py
python graph_rag/graph_rag.py
```

---

### **Run FastAPI Service**

```bash
uvicorn api.main:app --reload
```

---

## 🔌 API Endpoints

### ✅ Health Check

```
GET /health
```

---

### 🔹 Traditional RAG

```
POST /traditional-rag
```

```json
{
  "query": "Who is the Lady in Silver?"
}
```

---

### 🔹 Graph RAG

```
POST /graph-rag
```

```json
{
  "query": "Who is the Lady in Silver and how is she connected to Lord Penwood?"
}
```

---

## 🧠 Key Insight

Traditional RAG retrieves **similar text chunks**.

Graph RAG retrieves **structured relationships and enables multi-hop reasoning**.

For this mystery, correct reasoning requires connecting entities:

```
Sophie Baek → Lady in Silver
Sophie Baek → Lord Penwood
```

Graph RAG makes these connections explicit and easier for the LLM to reason over.

---

## 📂 Data

* `data/documents.txt` — Text corpus
* `data/graph.json` — Knowledge graph

---

## ⚡ Improvements Over Previous Version

* ✅ Replaced Ollama with **OpenAI APIs**
* ✅ Added **secure API key management using .env**
* ✅ Upgraded to **production-grade embeddings (text-embedding-3-small)**
* ✅ Improved reasoning using **gpt-4.1-mini**
* ✅ Added **FastAPI RAG service layer**
* ✅ Clean, scalable architecture (API-ready)

---

## 🚀 Next Steps (Optional Enhancements)

* Persist FAISS index (avoid recomputation)
* Build **Hybrid RAG (Graph + Vector)**
* Add **Docker + CI/CD pipeline**
* Add caching (Redis) and async processing

---

## 💡 Summary

This project demonstrates how:

* Traditional RAG is great for **semantic retrieval**
* Graph RAG excels at **relationship-aware reasoning**
* FastAPI enables **production-ready AI services**
* Combining both leads to **real-world AI backend systems**

---

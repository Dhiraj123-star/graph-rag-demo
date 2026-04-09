# Graph RAG vs Traditional RAG Demo

Minimal comparison of **Traditional RAG**, **Graph RAG**, and **Hybrid RAG** using the Bridgerton "Lady in Silver" mystery — powered by **OpenAI APIs** and exposed via a **FastAPI service**.

---

## ❓ Question

Who is the Lady in Silver and how is she connected to Lord Penwood?

---

## 🎯 Purpose

All systems use the same facts but different representations:

### **Traditional RAG**

* Stores text chunks
* Retrieves using vector similarity (FAISS)
* Uses **OpenAI embeddings** for semantic search

### **Graph RAG**

* Stores entities and relationships
* Retrieves using graph traversal (multi-hop reasoning)
* Uses **OpenAI LLM for reasoning**

### **Hybrid RAG (NEW)**

* Combines **vector search + graph relationships**
* Uses text for context and graph for reasoning
* Provides **more accurate and explainable answers**

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

### 🔹 Hybrid RAG (NEW 🚀)

```
POST /hybrid-rag
```

```json
{
  "query": "Who is the Lady in Silver and how is she connected to Lord Penwood?"
}
```

---

## 🧠 Key Insight

* Traditional RAG retrieves **similar text chunks**
* Graph RAG retrieves **structured relationships (multi-hop reasoning)**
* Hybrid RAG combines both for **better accuracy and reasoning**

For this mystery, correct reasoning requires connecting entities:

```
Sophie Baek → Lady in Silver
Sophie Baek → Lord Penwood
```

Graph relationships provide the reasoning path, while vector search provides supporting context.

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
* ✅ Introduced **Hybrid RAG (Graph + Vector)**
* ✅ Clean, scalable architecture (API-ready)

---

## 🚀 Next Steps (Optional Enhancements)

* Persist FAISS index (avoid recomputation)
* Add **Redis caching**
* Implement **async endpoints**
* Add **Docker + CI/CD pipeline**
* Improve entity extraction (NER / LLM-based)

---

## 💡 Summary

This project demonstrates how:

* Traditional RAG is great for **semantic retrieval**
* Graph RAG excels at **relationship-aware reasoning**
* Hybrid RAG delivers **best of both worlds**
* FastAPI enables **production-ready AI services**

---


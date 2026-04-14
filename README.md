# Graph RAG vs Traditional RAG Demo

Minimal comparison of **Traditional RAG**, **Graph RAG**, and **Hybrid RAG** using the Bridgerton "Lady in Silver" mystery — powered by **OpenAI APIs** and exposed via a **FastAPI service**, now with **NGINX reverse proxy and HTTPS support**.

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

### **Hybrid RAG**

* Combines **vector search + graph relationships**
* Uses text for context and graph for reasoning
* Provides **more accurate and explainable answers**

---

## 🧰 Tech Stack

* **LLM**: OpenAI (`gpt-4.1-mini`)
* **Embeddings**: OpenAI (`text-embedding-3-small`)
* **Vector Search**: FAISS (with persistence)
* **Graph Storage**: JSON
* **API Layer**: FastAPI (async-enabled)
* **Reverse Proxy**: NGINX
* **Security**: HTTPS (self-signed SSL)
* **Containerization**: Docker + Docker Compose
* **Environment**: uv / venv
* **Config Management**: python-dotenv (.env)

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env id="env123"
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Make sure `.env` is added to `.gitignore`

---

## ⚙️ Setup (Local Development)

```bash id="setup1"
cd graph-rag-bridgerton-demo
```

```bash id="setup2"
uv venv
source .venv/bin/activate
```

```bash id="setup3"
uv sync
```

---

## ▶️ Run

### **Run Scripts (Standalone)**

```bash id="run1"
python traditional_rag/rag.py
python graph_rag/graph_rag.py
```

---

### **Run FastAPI Service**

```bash id="run2"
uvicorn api.main:app --reload
```

---

## 🐳 Run with Docker + NGINX + HTTPS (Recommended)

### 🔐 Step 1: Generate SSL Certificate

```bash id="ssl1"
mkdir -p nginx/ssl

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout nginx/ssl/key.pem \
-out nginx/ssl/cert.pem
```

---

### 🚀 Step 2: Build & Run

```bash id="docker1"
docker-compose up --build
```

---

### 🛑 Stop

```bash id="docker2"
docker-compose down
```

---

## 🌐 Access Application

### 🔒 HTTPS (Primary)

```bash id="url1"
https://localhost/docs
```

### 🔁 HTTP (Auto Redirect)

```bash id="url2"
http://localhost → redirects to HTTPS
```

> ⚠️ Browser will show a warning for self-signed certificates → click **Advanced → Proceed**

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

```json id="req1"
{
  "query": "Who is the Lady in Silver?"
}
```

---

### 🔹 Graph RAG

```
POST /graph-rag
```

```json id="req2"
{
  "query": "Who is the Lady in Silver and how is she connected to Lord Penwood?"
}
```

---

### 🔹 Hybrid RAG 🚀

```
POST /hybrid-rag
```

```json id="req3"
{
  "query": "Who is the Lady in Silver and how is she connected to Lord Penwood?"
}
```

---

## 🧠 Key Insight

* Traditional RAG retrieves **similar text chunks**
* Graph RAG retrieves **structured relationships (multi-hop reasoning)**
* Hybrid RAG combines both for **better accuracy and reasoning**

```
Sophie Baek → Lady in Silver  
Sophie Baek → Lord Penwood
```

Graph relationships provide reasoning, vector search provides supporting context.

---

## 📂 Data

* `data/documents.txt` — Text corpus
* `data/graph.json` — Knowledge graph
* `data/faiss.index` — Persisted FAISS index
* `data/embeddings.npy` — Cached embeddings

> 📌 Persisted using Docker volumes

---

## ⚡ Improvements Over Previous Version

* ✅ Replaced Ollama with **OpenAI APIs**
* ✅ Added **secure API key management using .env**
* ✅ Upgraded embeddings (`text-embedding-3-small`)
* ✅ Improved reasoning (`gpt-4.1-mini`)
* ✅ FastAPI async API layer
* ✅ Hybrid RAG (Graph + Vector)
* ✅ FAISS persistence
* ✅ Dockerized with Compose
* ✅ Added **NGINX reverse proxy**
* ✅ Enabled **HTTPS with self-signed SSL**

---

## 🚀 Next Steps (Optional Enhancements)

* Add **CI/CD pipeline (GitHub Actions)**
* Replace self-signed SSL with **Let's Encrypt (production)**
* Deploy on **AWS / Kubernetes**
* Add **rate limiting + caching (Redis)**

---

## 💡 Summary

This project demonstrates:

* Semantic retrieval (**Traditional RAG**)
* Relationship reasoning (**Graph RAG**)
* Combined intelligence (**Hybrid RAG**)
* Scalable backend (**FastAPI + Async**)
* Persistent vector storage (**FAISS**)
* Production-ready deployment (**Docker + NGINX + HTTPS**)

---

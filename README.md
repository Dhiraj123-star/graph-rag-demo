# Graph RAG vs Traditional RAG Demo

Minimal comparison of **Traditional RAG**, **Graph RAG**, and **Hybrid RAG** using the Bridgerton "Lady in Silver" mystery — powered by **OpenAI APIs** and exposed via a **FastAPI service**, now enhanced with **NGINX, HTTPS, Redis caching, and rate limiting**.

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
* **Caching Layer**: Redis
* **Rate Limiting**: SlowAPI
* **Containerization**: Docker + Docker Compose
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

## ⚙️ Setup (Local Development)

```bash
cd graph-rag-bridgerton-demo
```

```bash
uv venv
source .venv/bin/activate
```

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

## 🐳 Run with Docker + NGINX + HTTPS (Recommended)

### 🔐 Step 1: Generate SSL Certificate

```bash
mkdir -p nginx/ssl

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout nginx/ssl/key.pem \
-out nginx/ssl/cert.pem
```

---

### 🚀 Step 2: Start Services

```bash
docker-compose up --build
```

---

### 🛑 Stop Services

```bash
docker-compose down
```

---

## 🌐 Access Application

### 🔒 HTTPS (Primary)

```bash
https://localhost/docs
```

### 🔁 HTTP (Auto Redirect)

```bash
http://localhost → redirects to HTTPS
```

> ⚠️ Browser warning for self-signed SSL is expected

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

### 🔹 Hybrid RAG 🚀

```
POST /hybrid-rag
```

```json
{
  "query": "Who is the Lady in Silver and how is she connected to Lord Penwood?"
}
```

---

## ⚡ Performance & Protection Enhancements

### 🚀 Redis Caching

* Caches responses for repeated queries (TTL: 5 minutes)
* Reduces OpenAI API calls
* Improves response time significantly

### 🚫 Rate Limiting

* Limit: **5 requests/minute per IP**
* Prevents abuse and API overuse

Example response when exceeded:

```json
{
  "error": "Rate limit exceeded"
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

Graph provides reasoning, vector provides context.

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
* ✅ Added **.env-based secure API key management**
* ✅ Upgraded embeddings (`text-embedding-3-small`)
* ✅ Improved reasoning (`gpt-4.1-mini`)
* ✅ Async FastAPI endpoints
* ✅ Hybrid RAG (Graph + Vector)
* ✅ FAISS persistence (no recomputation)
* ✅ Dockerized with Compose
* ✅ NGINX reverse proxy
* ✅ HTTPS (self-signed SSL)
* ✅ Redis caching layer
* ✅ Rate limiting (SlowAPI)

---

## 🚀 Next Steps (Optional Enhancements)

* Add **CI/CD pipeline (GitHub Actions)**
---

## 💡 Summary

This project demonstrates:

* Semantic retrieval (**Traditional RAG**)
* Relationship reasoning (**Graph RAG**)
* Combined intelligence (**Hybrid RAG**)
* High-performance APIs (**Async FastAPI**)
* Optimized responses (**Redis caching**)
* API protection (**Rate limiting**)
* Scalable deployment (**Docker + NGINX + HTTPS**)

---

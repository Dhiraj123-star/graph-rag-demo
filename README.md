# 🚀 Graph RAG vs Traditional RAG Demo

Minimal comparison of **Traditional RAG**, **Graph RAG**, and **Hybrid RAG** using the Bridgerton *"Lady in Silver"* mystery — powered by **OpenAI APIs** and deployed as a **production-ready FastAPI service** with **NGINX, HTTPS, Redis, Rate Limiting, and CI/CD**.

---

## ❓ Question

Who is the Lady in Silver and how is she connected to Lord Penwood?

---

## 🎯 Purpose

All systems use the same facts but different representations:

### 🔹 Traditional RAG

* Stores text chunks
* Retrieves using vector similarity (FAISS)
* Uses OpenAI embeddings

### 🔹 Graph RAG

* Stores entities & relationships
* Uses multi-hop reasoning
* Better for structured understanding

### 🔹 Hybrid RAG

* Combines vector + graph
* Uses **text for context + graph for reasoning**
* Most accurate & explainable

---

## 🧰 Tech Stack

* **LLM**: OpenAI (`gpt-4.1-mini`)
* **Embeddings**: OpenAI (`text-embedding-3-small`)
* **Vector DB**: FAISS (persistent)
* **Graph Storage**: JSON
* **API Layer**: FastAPI (async)
* **Reverse Proxy**: NGINX
* **Security**: HTTPS (self-signed SSL)
* **Caching**: Redis
* **Rate Limiting**: SlowAPI
* **Containerization**: Docker + Docker Compose
* **CI/CD**: GitHub Actions → DockerHub
* **Config**: python-dotenv

---

## 🔐 Environment Setup

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ⚙️ Local Setup

```bash
cd graph-rag-bridgerton-demo
uv venv
source .venv/bin/activate
uv sync
```

---

## ▶️ Run Locally

```bash
uvicorn api.main:app --reload
```

---

## 🐳 Run with Docker + NGINX + HTTPS

### 🔐 Generate SSL

```bash
mkdir -p nginx/ssl

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout nginx/ssl/key.pem \
-out nginx/ssl/cert.pem
```

---

### 🚀 Start Services

```bash
docker-compose up --build
```

---

### 🌐 Access

* 🔒 [https://localhost/docs](https://localhost/docs)
* 🔁 [http://localhost](http://localhost) → auto redirects

---

## 🔌 API Endpoints

### ✅ Health

```
GET /health
```

### 🔹 Traditional RAG

```
POST /traditional-rag
```

### 🔹 Graph RAG

```
POST /graph-rag
```

### 🔹 Hybrid RAG 🚀

```
POST /hybrid-rag
```

---

## ⚡ Performance & Protection

### 🚀 Redis Caching

* TTL: 5 minutes
* Reduces OpenAI calls
* Faster responses

### 🚫 Rate Limiting

* 5 requests/min/IP
* Prevents abuse

---

## 🧠 Key Insight

```
Sophie Baek → Lady in Silver  
Sophie Baek → Lord Penwood
```

* Graph → reasoning
* Vector → supporting context
* Hybrid → best results

---

## 📂 Data

* `data/documents.txt`
* `data/graph.json`
* `data/faiss.index`
* `data/embeddings.npy`

📌 Persisted via Docker volumes

---

## ⚡ Production Improvements

* ✅ OpenAI APIs (LLM + embeddings)
* ✅ Async FastAPI endpoints
* ✅ Hybrid RAG (Graph + Vector)
* ✅ FAISS persistence
* ✅ Redis caching
* ✅ Rate limiting
* ✅ Dockerized (~59MB optimized image)
* ✅ NGINX reverse proxy
* ✅ HTTPS (self-signed SSL)
* ✅ CI/CD with GitHub Actions
* ✅ Auto push to DockerHub

---

## 🔄 CI/CD Pipeline

On every push to `main`:

* Build Docker image
* Push to DockerHub (`dhiraj918106/rag-api`)
* Ready for deployment

---

## 🚀 Next Steps

* Use **Let's Encrypt SSL (production)**
* Deploy on **AWS / Kubernetes**
* Add **observability (Prometheus + Grafana)**

---

## 💡 Summary

This project demonstrates:

* Semantic search → **Traditional RAG**
* Relationship reasoning → **Graph RAG**
* Combined intelligence → **Hybrid RAG**
* High performance → **Async FastAPI + Redis**
* Secure deployment → **NGINX + HTTPS**
* DevOps maturity → **Docker + CI/CD**

---

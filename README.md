# KnowledgeRouter

**One-line:** KnowledgeRouter — multi-model RAG assistant with intent-based routing and agent automation.

---

## Demo
- Live demo (if deployed): *(add your URL here)*  
- Quick demo video (90s): `demo_video.mp4` (or add Loom/YouTube link)

---

## Elevator pitch
KnowledgeRouter ingests team docs (PDF, Markdown, Confluence exports), builds a searchable vector index, and serves a single API that (1) chooses the best model per query (local Llama / hosted LLM / low-cost fallback) based on intent, cost and latency targets, (2) performs retrieval-augmented answering, and (3) when allowed, runs a safe automation agent (e.g., summarize + draft reply) to save engineers' time.

---

## Why this project matters (signal to recruiters)
- Demonstrates full-stack ML engineering: ingestion pipelines, embeddings, vector indexing, model routing, and safe agent orchestration.  
- Shows production tradeoffs: latency vs cost, caching, batching, fallback policies, and observability.  
- Highlights MLOps & infra skills: containerized serving, CI, tests, deployment scripts, and reproducible pipelines.

---

## Features
- Document ingestion (`/ingest`) — supports `.txt`, `.md`, `.pdf`.  
- Chunking & overlap with metadata (source, page, section).  
- Embeddings via `sentence-transformers` (pluggable to OpenAI embeddings).  
- Vector store: FAISS (on-disk) with simple sharding plugin.  
- Retriever: top-k + reranker (optional lightweight re-ranker).  
- Multi-LLM Router:
  - Intent classifier routes queries to: **cheap short-answer model**, **large-context model**, **private Llama** (if available), or **hosted API** (OpenAI/Anthropic).
  - Fallbacks & retry logic for availability and cost optimization.  
- Agent orchestration:
  - Safe tools (summarize, draft_email, metadata_lookup), sandboxed action execution, human-in-the-loop confirmation for destructive actions.  
- FastAPI backend with async request handling.  
- Dockerized for local dev + example GitHub Actions CI pipeline.  
- Basic metrics: p95 latency, cache hit-rate, cost-per-query estimation.

---

## Architecture
![architecture diagram](architecture.png)

**Components**
1. `api/` — FastAPI service that exposes ingest/query endpoints and orchestrates routing & agents.  
2. `ingest/` — pipeline for parsing, chunking, embedding, indexing.  
3. `vectorstore/` — FAISS index manager + metadata store (sqlite/postgres).  
4. `router/` — intent classifier + routing policy (rules + ML).  
5. `llm_clients/` — adapters for local HF models, OpenAI, Anthropic.  
6. `agents/` — tool definitions and safe executor.  
7. `infra/` — docker-compose, example cloud deployment (Cloud Run / Render / VM), optional Terraform.  
8. `observability/` — Prometheus metrics exporter + simple Grafana dashboard config (optional).

---

## Tech stack
- Python 3.11  
- FastAPI, Uvicorn, Pydantic  
- PyTorch (for local models), Hugging Face Transformers  
- sentence-transformers (embeddings)  
- FAISS (vector index)  
- Docker, Docker Compose  
- GitHub Actions (CI)  
- Optional: Redis (cache), Postgres (metadata), Sentry (errors), Prometheus/Grafana (metrics)

---

## Quickstart — local (Docker)
> Assumes Git and Docker are installed.

```bash
# clone
git clone https://github.com/<you>/knowledgerouter.git
cd knowledgerouter

# copy example env and edit keys (OPENAI_API_KEY optional)
cp .env.example .env

# build & run
docker compose up --build

# open docs
# visit http://localhost:8000/docs
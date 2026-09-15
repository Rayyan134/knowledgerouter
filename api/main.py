from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import uuid
import json
import os

app = FastAPI(title="KnowledgeRouter - API Skeleton")

# Simple in-memory "index" placeholder
DOC_STORE = {}

class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 4
    enable_agent: Optional[bool] = False

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), metadata: Optional[str] = None):
    """Accepts a text/markdown/pdf file — for now we read text and store content."""
    filename = file.filename
    contents = await file.read()
    try:
        text = contents.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode file")
    doc_id = str(uuid.uuid4())
    DOC_STORE[doc_id] = {"filename": filename, "text": text, "metadata": metadata}
    return {"status": "ok", "doc_id": doc_id, "filename": filename}

@app.post("/query")
async def query(req: QueryRequest):
    """Very small demo retrieval: returns best-matching doc by substring score."""
    q = req.query.lower()
    # naive scoring: count overlap words
    scores = []
    for doc_id, doc in DOC_STORE.items():
        score = sum(1 for w in q.split() if w in doc["text"].lower())
        scores.append((score, doc_id))
    scores.sort(reverse=True)
    top = []
    for score, doc_id in scores[: req.k]:
        if score <= 0:
            continue
        doc = DOC_STORE[doc_id]
        top.append({"doc_id": doc_id, "filename": doc["filename"], "snippet": doc["text"][:400], "score": score})
    answer = "No good match found." if not top else f"Found {len(top)} candidate(s)."
    return {"answer": answer, "candidates": top, "route": {"model": "local-skeleton", "rationale": "demo"}}

@app.get("/health")
def health():
    return {"status": "ok", "docs_indexed": len(DOC_STORE)}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
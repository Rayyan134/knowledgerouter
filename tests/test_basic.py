from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()

def test_ingest_and_query():
    # ingest a simple text file
    files = {"file": ("hello.txt", b"Hello world. This is a test document about API keys.")}
    r = client.post("/ingest", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "doc_id" in data

    # query for a token that exists
    q = {"query": "API keys"}
    r2 = client.post("/query", json=q)
    assert r2.status_code == 200
    assert "answer" in r2.json()
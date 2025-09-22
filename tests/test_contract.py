from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def check(path: str):
    r = client.post(path, json={"prompt": "sanity"})
    assert r.status_code == 200, r.text
    d = r.json()
    for k in ("answer", "sources", "chunks"):
        assert k in d
    assert isinstance(d["answer"], str)
    assert isinstance(d["sources"], list)
    assert isinstance(d["chunks"], list)

def test_contract_all():
    for p in ("/rag-real", "/rag-fake", "/rag-with-filter", "/rag-debug"):
        check(p)

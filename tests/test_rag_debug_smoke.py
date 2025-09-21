from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rag_debug_shape():
    r = client.post("/rag-debug", json={"prompt": "sanity"})
    assert r.status_code == 200, r.text
    data = r.json()
    for k in ("answer", "sources", "chunks"):
        assert k in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["chunks"], list)
    if data["chunks"]:
        assert isinstance(data["chunks"][0], dict)
        assert "content" in data["chunks"][0]

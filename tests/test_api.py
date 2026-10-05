from fastapi.testclient import TestClient
import pytest

import app.main as api
from app.search import SearchHit


class StubSearcher:
    size = 3

    @classmethod
    def from_corpus(cls, corpus_path):
        return cls()

    def search(self, query, mode="hybrid", top_k=10, rrf_k=60):
        return [SearchHit("cloud_001", "Cloud", "A cloud document", 0.75)][:top_k]


@pytest.fixture
def client(monkeypatch, tmp_path):
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(api, "CORPUS_PATH", corpus)
    monkeypatch.setattr(api, "Searcher", StubSearcher)
    with TestClient(api.app) as test_client:
        yield test_client


def test_search_returns_response_schema_and_latency(client):
    response = client.get("/search", params={"q": "cloud scaling", "mode": "hybrid"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "cloud scaling"
    assert body["mode"] == "hybrid"
    assert body["top_k"] == 10
    assert isinstance(body["latency_ms"], float)
    assert body["latency_ms"] >= 0
    assert body["hits"] == [{
        "doc_id": "cloud_001",
        "title": "Cloud",
        "text": "A cloud document",
        "score": 0.75,
    }]


@pytest.mark.parametrize("params", [
    {"q": "cloud", "mode": "kw"},
    {"q": "cloud", "mode": "invalid"},
    {"q": "cloud", "top_k": 0},
    {"q": "cloud", "top_k": 101},
])
def test_invalid_mode_and_top_k_are_rejected(client, params):
    response = client.get("/search", params=params)

    assert response.status_code == 422

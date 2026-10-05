import pytest

from app.search import Searcher, SearchHit


def test_rrf_combines_one_based_ranks_and_unique_candidates(monkeypatch):
    searcher = Searcher()
    hit = lambda doc: SearchHit(doc, doc, doc, 1.0)
    monkeypatch.setattr(searcher, "_search_keyword", lambda q, k: [hit("a"), hit("b")])
    monkeypatch.setattr(searcher, "_search_semantic", lambda q, k: [hit("b"), hit("c")])

    results = searcher.search("example", mode="hybrid", top_k=3)

    assert [h.doc_id for h in results] == ["b", "a", "c"]
    assert results[0].score == pytest.approx(1 / 62 + 1 / 61)
    assert results[1].score == pytest.approx(1 / 61)
    assert results[2].score == pytest.approx(1 / 62)

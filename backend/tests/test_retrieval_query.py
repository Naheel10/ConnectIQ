import uuid

from app.services.retrieval import build_similarity_query


def test_similarity_query_has_limit():
    query = build_similarity_query(uuid.uuid4(), [0.0] * 1536, top_k=7)
    sql = str(query)
    assert 'LIMIT' in sql

from sqlalchemy import Select, desc, select, text
from sqlalchemy.orm import Session

from app.models.entities import Document
from app.services.embeddings import embed_text


def build_similarity_query(tenant_id, embedding: list[float], top_k: int = 5) -> Select:
    return (
        select(Document)
        .where(Document.tenant_id == tenant_id)
        .order_by(Document.embedding.cosine_distance(embedding))
        .limit(top_k)
    )


def retrieve_documents(db: Session, tenant_id, question: str, top_k: int = 5) -> list[Document]:
    q_embedding = embed_text(question)
    query = build_similarity_query(tenant_id, q_embedding, top_k=top_k)
    return list(db.execute(query).scalars().all())


def classify_query(question: str) -> str:
    lower = question.lower()
    if 'forecast' in lower and 'stage' in lower:
        return 'forecast_by_stage'
    if 'at risk' in lower or 'stalled' in lower:
        return 'at_risk'
    return 'general'

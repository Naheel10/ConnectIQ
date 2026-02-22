from langchain_openai import ChatOpenAI

from app.core.config import get_settings
from app.services.retrieval import classify_query, retrieve_documents

settings = get_settings()


def generate_chat_response(db, tenant_id, message: str) -> dict:
    docs = retrieve_documents(db, tenant_id, message, top_k=6)
    mode = classify_query(message)
    context = '\n\n'.join([f"[{d.source_type}:{d.source_sf_id}] {d.content}" for d in docs])
    system_prompt = (
        'You are a CRM analyst assistant. Answer using only the provided sources. '
        'If sources are insufficient, say you do not know. Keep concise and factual.'
    )
    if settings.openai_api_key:
        llm = ChatOpenAI(model=settings.openai_chat_model, api_key=settings.openai_api_key, temperature=0)
        answer = llm.invoke([
            ('system', system_prompt),
            ('human', f"Question: {message}\nQuery mode: {mode}\nSources:\n{context}"),
        ]).content
    else:
        answer = f"Demo mode response (no OpenAI key). Query mode={mode}. Based on {len(docs)} retrieved records."

    citations = []
    for d in docs[:4]:
        metadata = d.metadata_json or {}
        display = metadata.get('name') or metadata.get('email_masked') or d.source_sf_id
        citations.append(
            {
                'source_type': d.source_type,
                'source_sf_id': d.source_sf_id,
                'display': display,
                'excerpt': d.content[:180],
            }
        )
    return {'answer': answer, 'citations': citations, 'retrieved': [d.content for d in docs]}

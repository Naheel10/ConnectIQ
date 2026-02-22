from openai import OpenAI

from app.core.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


def embed_text(text: str) -> list[float]:
    if not client:
        return [0.0] * 1536
    resp = client.embeddings.create(model=settings.openai_embedding_model, input=text)
    return resp.data[0].embedding

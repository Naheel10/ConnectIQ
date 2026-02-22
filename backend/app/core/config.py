from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'ConnectIQ'
    environment: str = 'dev'
    app_secret_key: str = 'dev-secret-change-me'

    database_url: str = 'postgresql+psycopg://connectiq:connectiq@db:5432/connectiq'

    openai_api_key: str = ''
    openai_embedding_model: str = 'text-embedding-3-small'
    openai_chat_model: str = 'gpt-4o-mini'

    demo_user_email: str = 'demo@connectiq.local'
    demo_user_password: str = 'password123'

    salesforce_client_id: str = ''
    salesforce_client_secret: str = ''
    salesforce_redirect_uri: str = 'http://localhost:8000/salesforce/oauth/callback'
    salesforce_login_url: str = 'https://login.salesforce.com'

    frontend_url: str = 'http://localhost:5173'
    auth_token_exp_minutes: int = 60 * 24


@lru_cache
def get_settings() -> Settings:
    return Settings()

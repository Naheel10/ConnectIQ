from fastapi import FastAPI
from sqlalchemy import select

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import SessionLocal
from app.models.entities import Tenant, User
from app.utils.security import hash_password

settings = get_settings()
configure_logging()
app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.on_event('startup')
def startup_seed():
    db = SessionLocal()
    try:
        tenant = db.scalar(select(Tenant).limit(1))
        if not tenant:
            tenant = Tenant(name='default')
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
        user = db.scalar(select(User).where(User.email == settings.demo_user_email))
        if not user:
            user = User(tenant_id=tenant.id, email=settings.demo_user_email, password_hash=hash_password(settings.demo_user_password))
            db.add(user)
            db.commit()
    finally:
        db.close()

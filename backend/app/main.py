import logging

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
logger = logging.getLogger(__name__)
app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.on_event('startup')
def startup_seed():
    db = SessionLocal()
    try:
        tenant = db.scalar(select(Tenant).where(Tenant.name == 'default').limit(1))
        tenant_action = 'unchanged'
        if not tenant:
            tenant = Tenant(name='default')
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            tenant_action = 'created'

        demo_email = settings.demo_user_email.strip()
        demo_password_hash = hash_password(settings.demo_user_password)

        user = db.scalar(select(User).where(User.email == demo_email))
        if not user:
            user = User(tenant_id=tenant.id, email=demo_email, password_hash=demo_password_hash)
            db.add(user)
            db.commit()
            user_action = 'created'
        else:
            user.password_hash = demo_password_hash
            db.add(user)
            db.commit()
            user_action = 'password_updated'

        logger.info('Startup seed complete: tenant=%s demo_user=%s email=%s', tenant_action, user_action, demo_email)
    finally:
        db.close()

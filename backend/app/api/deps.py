from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Tenant, User
from app.utils.security import decode_token

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> User:
    if not cred:
        raise HTTPException(status_code=401, detail='Missing token')
    payload = decode_token(cred.credentials)
    user = db.scalar(select(User).where(User.email == payload['sub']))
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    return user


def get_tenant_id(user: User = Depends(get_current_user)):
    return user.tenant_id

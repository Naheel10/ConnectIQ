import base64
import hashlib
from datetime import datetime, timedelta, timezone

from cryptography.fernet import Fernet
from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_token_exp_minutes)
    payload = {'sub': subject, 'exp': expire}
    return jwt.encode(payload, settings.app_secret_key, algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.app_secret_key, algorithms=['HS256'])


def _fernet_key() -> bytes:
    digest = hashlib.sha256(settings.app_secret_key.encode()).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_value(value: str) -> str:
    return Fernet(_fernet_key()).encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    return Fernet(_fernet_key()).decrypt(value.encode()).decode()

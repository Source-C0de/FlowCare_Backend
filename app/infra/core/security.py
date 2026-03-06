"""
Security/auth placeholder.

In production you can add JWT/OAuth2, RBAC, API keys, etc.
"""
import base64
import pwd
from fastapi import security
from passlib.context import CryptContext


# use pbkdf2_sha256 to avoid bcrypt 72-byte password backend limits
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = security.HTTPBasic()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str)-> bool:
    return pwd_context.verify(plain, hashed)



from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import bcrypt
import jwt
from app.core.config import get_settings

settings = get_settings()


class Security:
    """مسؤول عن التشفير والمصادقة"""

    @staticmethod
    def _prepare_password(password: str) -> bytes:
        """
        bcrypt له حد أقصى 72 بايت. نستخدم SHA-256 أولاً
        لتحويل أي كلمة سر إلى 32 بايت ثابتة، ثم نمررها لـ bcrypt.
        هذا يحل مشكلة الكلمات الطويلة والرموز التعبيرية.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")

    @staticmethod
    def hash_password(password: str) -> str:
        """تشفير كلمة السر قبل الحفظ"""
        prepared = Security._prepare_password(password)
        hashed = bcrypt.hashpw(prepared, bcrypt.gensalt(rounds=12))
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """التحقق من مطابقة كلمة السر"""
        try:
            prepared = Security._prepare_password(plain)
            return bcrypt.checkpw(prepared, hashed.encode("utf-8"))
        except Exception:
            return False

    @staticmethod
    def create_access_token(user_id: int, username: str, role: str) -> str:
        """توليد JWT للمستخدم"""
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """فك تشفير JWT وإرجاع البيانات"""
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    COOKIE_NAME = "access_token"

    @staticmethod
    def set_token_cookie(response, token: str, max_age: int) -> None:
        response.set_cookie(
            key=Security.COOKIE_NAME,
            value=token,
            max_age=max_age,
            httponly=True,
            samesite="lax",
            secure=False,  # في الإنتاج اجعلها True مع HTTPS
            path="/",
        )

    @staticmethod
    def delete_token_cookie(response) -> None:
        response.delete_cookie(Security.COOKIE_NAME, path="/")
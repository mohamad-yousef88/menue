from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import Security
from app.models import User


def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)) -> User | None:
    """يقرأ JWT من الكوكي ويعيد المستخدم أو None"""
    token = request.cookies.get(Security.COOKIE_NAME)
    if not token:
        return None
    payload = Security.decode_token(token)
    if not payload:
        return None
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        return None
    return user
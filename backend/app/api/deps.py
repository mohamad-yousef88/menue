from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import Security
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.services.menu_service import MenuService
from app.services.menu_item_service import MenuItemService
from app.services.auth_service import AuthService
from app.models import User

# مخطط الأمان (يظهر زر Authorize في Swagger)
bearer_scheme = HTTPBearer(auto_error=False)


def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(db)


def get_menu_item_service(db: Session = Depends(get_db)) -> MenuItemService:
    return MenuItemService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """يجلب المستخدم الحالي من JWT"""
    if not credentials:
        raise UnauthorizedException("يجب تسجيل الدخول للقيام بهذا الإجراء")

    payload = Security.decode_token(credentials.credentials)
    if not payload:
        raise UnauthorizedException("الجلسة منتهية أو الرمز غير صالح")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise UnauthorizedException("المستخدم غير موجود أو غير مفعّل")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """يتأكد أن المستخدم أدمن"""
    if current_user.role != "admin":
        raise ForbiddenException("هذا الإجراء للأدمن فقط")
    return current_user
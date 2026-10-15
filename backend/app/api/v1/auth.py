from fastapi import APIRouter, Depends, status
from typing import List
from app.api.deps import get_auth_service, get_current_user
from app.services.auth_service import AuthService
from app.schemas.auth import (
    LoginRequest, RegisterRequest, TokenResponse,
    UserResponse, ChangePasswordRequest,
)
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/setup-required")
def setup_required(service: AuthService = Depends(get_auth_service)):
    """هل التطبيق بحاجة لأول مستخدم؟"""
    return {"setup_required": service.needs_setup()}


@router.post("/setup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def setup_first_user(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    """إنشاء أول أدمن (يعمل مرة واحدة فقط)"""
    return service.register_first_user(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    """تسجيل الدخول وإرجاع JWT"""
    return service.login(data)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_user),
):
    """إضافة مستخدم جديد (يتطلب تسجيل الدخول)"""
    return service.register(data)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """معلومات المستخدم الحالي"""
    return current_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    data: ChangePasswordRequest,
    service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_user),
):
    """تغيير كلمة السر"""
    service.change_password(current_user.id, data)
    return {"message": "تم تغيير كلمة السر بنجاح"}


@router.get("/users", response_model=List[UserResponse])
def list_users(
    service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_user),
):
    """قائمة كل المستخدمين"""
    return service.list_users()
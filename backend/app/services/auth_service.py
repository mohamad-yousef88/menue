from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse, ChangePasswordRequest
from app.core.security import Security
from app.core.exceptions import UnauthorizedException, BadRequestException, ConflictException, NotFoundException
from app.core.config import get_settings

settings = get_settings()


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def needs_setup(self) -> bool:
        """هل هذه أول مرة (لا يوجد أي مستخدم)؟"""
        return self.repo.count() == 0

    def register_first_user(self, data: RegisterRequest) -> User:
        """إنشاء أول مستخدم (فقط إذا لا يوجد مستخدمون)"""
        if self.repo.count() > 0:
            raise ConflictException("يوجد مستخدم بالفعل، استخدم /register المحمي")
        user = User(
            username=data.username,
            password_hash=Security.hash_password(data.password),
            full_name=data.full_name,
            role="admin",
        )
        return self.repo.create(user)

    def register(self, data: RegisterRequest) -> User:
        """إضافة مستخدم جديد (يجب أن يكون المُنشئ مسجلاً)"""
        if self.repo.get_by_username(data.username):
            raise ConflictException("اسم المستخدم موجود مسبقاً")
        user = User(
            username=data.username,
            password_hash=Security.hash_password(data.password),
            full_name=data.full_name,
            role="manager",
        )
        return self.repo.create(user)

    def login(self, data: LoginRequest) -> TokenResponse:
        """تسجيل الدخول وإرجاع JWT"""
        user = self.repo.get_by_username(data.username)
        if not user or not Security.verify_password(data.password, user.password_hash):
            raise UnauthorizedException("اسم المستخدم أو كلمة السر غير صحيحة")
        if not user.is_active:
            raise UnauthorizedException("الحساب غير مفعّل")

        user.last_login = datetime.now()
        self.repo.update(user)

        token = Security.create_access_token(user.id, user.username, user.role)
        return TokenResponse(
            access_token=token,
            expires_in=settings.jwt_expire_minutes * 60,
        )

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise NotFoundException("المستخدم غير موجود")
        return user

    def change_password(self, user_id: int, data: ChangePasswordRequest) -> None:
        user = self.get_by_id(user_id)
        if not Security.verify_password(data.old_password, user.password_hash):
            raise BadRequestException("كلمة السر القديمة غير صحيحة")
        user.password_hash = Security.hash_password(data.new_password)
        self.repo.update(user)

    def list_users(self) -> list[User]:
        return self.repo.get_all()
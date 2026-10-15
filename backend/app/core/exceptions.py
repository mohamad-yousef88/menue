from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "العنصر غير موجود"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "طلب غير صالح"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "تعارض في البيانات"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ImageUploadException(HTTPException):
    def __init__(self, detail: str = "فشل رفع الصورة"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "يجب تسجيل الدخول"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "ليس لديك صلاحية"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
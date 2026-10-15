import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config import get_settings
from app.core.exceptions import ImageUploadException

settings = get_settings()

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


class ImageService:
    @staticmethod
    def upload(file: UploadFile, folder: str = "menu_items") -> dict:
        try:
            result = cloudinary.uploader.upload(file.file, folder=folder)
            return {
                "url": result["secure_url"],
                "public_id": result["public_id"],
            }
        except Exception as e:
            raise ImageUploadException(f"فشل رفع الصورة: {str(e)}")

    @staticmethod
    def delete(public_id: str) -> bool:
        if not public_id:
            return False
        try:
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception:
            return False
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.menu_item_repository import MenuItemRepository
from app.models import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate
from app.services.image_service import ImageService
from app.core.exceptions import NotFoundException


class MenuItemService:
    def __init__(self, db: Session):
        self.repo = MenuItemRepository(db)

    def list_by_menu(
        self,
        menu_id: int,
        category: Optional[str] = None,
        only_available: bool = False,
    ) -> List[MenuItem]:
        return self.repo.get_by_menu(menu_id, category, only_available)

    def get(self, item_id: int) -> MenuItem:
        item = self.repo.get(item_id)
        if not item:
            raise NotFoundException("العنصر غير موجود")
        return item

    def create(self, menu_id: int, data: MenuItemCreate, image_file=None) -> MenuItem:
        image_url = None
        image_public_id = None

        if image_file:
            result = ImageService.upload(image_file)
            image_url = result["url"]
            image_public_id = result["public_id"]

        item = MenuItem(
            **data.model_dump(),
            menu_id=menu_id,
            image_url=image_url,
            image_public_id=image_public_id,
        )
        return self.repo.create(item)

    def update(self, item_id: int, data: MenuItemUpdate, image_file=None) -> MenuItem:
        item = self.get(item_id)

        if image_file:
            if item.image_public_id:
                ImageService.delete(item.image_public_id)
            result = ImageService.upload(image_file)
            item.image_url = result["url"]
            item.image_public_id = result["public_id"]

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        return self.repo.update(item)

    def delete(self, item_id: int) -> None:
        item = self.get(item_id)
        if item.image_public_id:
            ImageService.delete(item.image_public_id)
        self.repo.delete(item)

    def get_categories(self, menu_id: int) -> List[str]:
        return self.repo.get_categories(menu_id)

    def count_by_menu(self, menu_id: int) -> int:
        return self.repo.count_by_menu(menu_id)

    def search(self, menu_id: int, query: str) -> List[MenuItem]:
        return self.repo.search(menu_id, query)
from typing import List
from sqlalchemy.orm import Session
from app.repositories.menu_repository import MenuRepository
from app.models import Menu
from app.schemas.menu import MenuCreate, MenuUpdate
from app.core.exceptions import NotFoundException
from app.services.image_service import ImageService


class MenuService:
    def __init__(self, db: Session):
        self.repo = MenuRepository(db)

    def list_all(self) -> List[Menu]:
        return self.repo.get_all()

    def get(self, menu_id: int) -> Menu:
        menu = self.repo.get(menu_id)
        if not menu:
            raise NotFoundException("المنيو غير موجود")
        return menu

    def get_default(self) -> Menu:
        menu = self.repo.get_default()
        if not menu:
            raise NotFoundException("لا يوجد منيو افتراضي")
        return menu

    def get_visible(self) -> Menu:
        menu = self.repo.get_visible_menu()
        if not menu:
            raise NotFoundException("لا يوجد منيو متاح للعرض")
        return menu

    def create(self, data: MenuCreate) -> Menu:
        if data.is_default:
            self.repo.unset_defaults()
        menu = Menu(**data.model_dump())
        return self.repo.create(menu)

    def update(self, menu_id: int, data: MenuUpdate) -> Menu:
        menu = self.get(menu_id)
        if data.is_default:
            self.repo.unset_defaults()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(menu, key, value)
        return self.repo.update(menu)

    def delete(self, menu_id: int) -> None:
        menu = self.get(menu_id)
        for item in menu.items:
            if item.image_public_id:
                ImageService.delete(item.image_public_id)
        self.repo.delete(menu)
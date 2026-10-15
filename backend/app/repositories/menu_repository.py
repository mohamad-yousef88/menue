from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Menu
from app.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    def __init__(self, db: Session):
        super().__init__(Menu, db)

    def get_default(self) -> Optional[Menu]:
        return self.db.query(Menu).filter(Menu.is_default == True).first()

    def get_active_menus(self) -> List[Menu]:
        now = datetime.now()
        return self.db.query(Menu).filter(
            Menu.is_active == True,
            (Menu.start_date.is_(None)) | (Menu.start_date <= now),
            (Menu.end_date.is_(None)) | (Menu.end_date >= now),
        ).all()

    def get_visible_menu(self) -> Optional[Menu]:
        active = self.get_active_menus()
        if active:
            return active[0]
        return self.get_default()

    def unset_defaults(self) -> None:
        self.db.query(Menu).filter(Menu.is_default == True).update({"is_default": False})
        self.db.commit()
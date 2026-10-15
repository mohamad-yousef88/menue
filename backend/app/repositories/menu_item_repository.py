from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import MenuItem
from app.repositories.base import BaseRepository


class MenuItemRepository(BaseRepository[MenuItem]):
    def __init__(self, db: Session):
        super().__init__(MenuItem, db)

    def get_by_menu(
        self,
        menu_id: int,
        category: Optional[str] = None,
        only_available: bool = False,
    ) -> List[MenuItem]:
        query = self.db.query(MenuItem).filter(MenuItem.menu_id == menu_id)
        if category and category != "الكل":
            query = query.filter(MenuItem.category == category)
        if only_available:
            query = query.filter(MenuItem.is_available == True)
        return query.order_by(MenuItem.sort_order, MenuItem.id).all()

    def get_categories(self, menu_id: int) -> List[str]:
        results = (
            self.db.query(MenuItem.category)
            .filter(MenuItem.menu_id == menu_id)
            .distinct()
            .all()
        )
        return [r[0] for r in results]

    def count_by_menu(self, menu_id: int) -> int:
        return self.db.query(MenuItem).filter(MenuItem.menu_id == menu_id).count()

    def search(self, menu_id: int, query: str) -> List[MenuItem]:
        like = f"%{query}%"
        return (
            self.db.query(MenuItem)
            .filter(
                MenuItem.menu_id == menu_id,
                (MenuItem.name.ilike(like)) | (MenuItem.description.ilike(like)),
            )
            .all()
        )
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.menu_item import MenuItemResponse


class MenuBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_default: bool = False
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MenuWithItems(MenuResponse):
    items: List[MenuItemResponse] = []
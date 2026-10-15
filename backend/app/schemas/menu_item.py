from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    price: int = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=50)
    is_available: bool = True
    is_featured: bool = False
    sort_order: int = 0


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None


class MenuItemResponse(MenuItemBase):
    id: int
    image_url: Optional[str] = None
    menu_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
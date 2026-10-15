from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    image_url = Column(String(500), nullable=True)
    image_public_id = Column(String(200), nullable=True)
    is_available = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    menu = relationship("Menu", back_populates="items")
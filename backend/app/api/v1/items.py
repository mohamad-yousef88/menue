from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from typing import List, Optional
from app.api.deps import get_menu_item_service, get_menu_service, get_current_user
from app.services.menu_item_service import MenuItemService
from app.services.menu_service import MenuService
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.models import User

router = APIRouter(prefix="/menus/{menu_id}/items", tags=["Menu Items"])


# ──────────── مسارات عامة (للزبون عبر QR) ────────────

@router.get("/public", response_model=List[MenuItemResponse])
def list_items_public(
    menu_id: int,
    category: Optional[str] = None,
    service: MenuItemService = Depends(get_menu_item_service),
):
    """عناصر المنيو للزبون - عام - يعرض المتوفر فقط"""
    return service.list_by_menu(menu_id, category, only_available=True)


@router.get("/categories/public", response_model=List[str])
def get_categories_public(
    menu_id: int,
    service: MenuItemService = Depends(get_menu_item_service),
):
    """الفئات للزبون - عام"""
    return service.get_categories(menu_id)


# ──────────── مسارات محمية (للموظف) ────────────

@router.get("/", response_model=List[MenuItemResponse])
def list_items(
    menu_id: int,
    category: Optional[str] = None,
    only_available: bool = False,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_by_menu(menu_id, category, only_available)


@router.get("/categories", response_model=List[str])
def get_categories(
    menu_id: int,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_categories(menu_id)


@router.get("/search", response_model=List[MenuItemResponse])
def search_items(
    menu_id: int,
    q: str,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    return service.search(menu_id, q)


@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    menu_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: int = Form(...),
    category: str = Form(...),
    is_available: bool = Form(True),
    is_featured: bool = Form(False),
    sort_order: int = Form(0),
    image: Optional[UploadFile] = File(None),
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    data = MenuItemCreate(
        name=name, description=description, price=price, category=category,
        is_available=is_available, is_featured=is_featured, sort_order=sort_order,
    )
    return service.create(menu_id, data, image)


@router.put("/{item_id}", response_model=MenuItemResponse)
def update_item(
    menu_id: int,
    item_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[int] = Form(None),
    category: Optional[str] = Form(None),
    is_available: Optional[bool] = Form(None),
    is_featured: Optional[bool] = Form(None),
    sort_order: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    data = MenuItemUpdate(
        name=name, description=description, price=price, category=category,
        is_available=is_available, is_featured=is_featured, sort_order=sort_order,
    )
    return service.update(item_id, data, image)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    menu_id: int,
    item_id: int,
    service: MenuItemService = Depends(get_menu_item_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(item_id)
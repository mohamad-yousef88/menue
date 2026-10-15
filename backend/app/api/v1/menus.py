from fastapi import APIRouter, Depends, status
from typing import List
from app.api.deps import get_menu_service, get_current_user
from app.services.menu_service import MenuService
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse, MenuWithItems
from app.models import User

router = APIRouter(prefix="/menus", tags=["Menus"])


# ──────────── مسارات عامة (للزبون - لا تحتاج تسجيل) ────────────

@router.get("/visible", response_model=MenuWithItems)
def get_visible_menu(service: MenuService = Depends(get_menu_service)):
    """المنيو المرئي للزبون عبر QR - عام"""
    return service.get_visible()


# ──────────── مسارات محمية (للموظف المسجّل) ────────────

@router.get("/", response_model=List[MenuResponse])
def list_menus(
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    """كل المنيوهات - يتطلب تسجيل دخول"""
    return service.list_all()


@router.get("/default", response_model=MenuWithItems)
def get_default_menu(
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_default()


@router.get("/{menu_id}", response_model=MenuWithItems)
def get_menu(
    menu_id: int,
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    return service.get(menu_id)


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    data: MenuCreate,
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(data)


@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(
    menu_id: int,
    data: MenuUpdate,
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(menu_id, data)


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
    menu_id: int,
    service: MenuService = Depends(get_menu_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(menu_id)
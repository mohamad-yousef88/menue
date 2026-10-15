from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from app.core.config import get_settings
from app.core.database import get_db
from app.web.deps import get_current_user_from_cookie
from app.services.menu_service import MenuService
from app.services.menu_item_service import MenuItemService
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate

router = APIRouter(prefix="/admin/menus/{menu_id}/items", tags=["Admin Items"])
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def list_items(menu_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    menu = MenuService(db).get(menu_id)
    items = MenuItemService(db).list_by_menu(menu_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/items.html",
        context={"user": user, "menu": menu, "items": items},
    )


@router.get("/new", response_class=HTMLResponse)
def new_item_form(menu_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    menu = MenuService(db).get(menu_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/item_form.html",
        context={"user": user, "menu": menu, "item": None},
    )


@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_item_form(menu_id: int, item_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    menu = MenuService(db).get(menu_id)
    item = MenuItemService(db).get(item_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/item_form.html",
        context={"user": user, "menu": menu, "item": item},
    )

@router.post("/save")
def save_item(
    menu_id: int,
    request: Request,
    item_id: Optional[int] = Form(None),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: int = Form(...),
    category: str = Form(...),
    is_available: bool = Form(False),
    is_featured: bool = Form(False),
    sort_order: int = Form(0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)

    service = MenuItemService(db)
    image_file = image if image and image.filename else None

    if item_id:
        service.update(item_id, MenuItemUpdate(
            name=name, description=description, price=price,
            category=category, is_available=is_available,
            is_featured=is_featured, sort_order=sort_order,
        ), image_file)
    else:
        service.create(menu_id, MenuItemCreate(
            name=name, description=description, price=price,
            category=category, is_available=is_available,
            is_featured=is_featured, sort_order=sort_order,
        ), image_file)

    return RedirectResponse(url=f"/admin/menus/{menu_id}/items", status_code=302)


@router.post("/{item_id}/delete")
def delete_item(menu_id: int, item_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    MenuItemService(db).delete(item_id)
    return RedirectResponse(url=f"/admin/menus/{menu_id}/items", status_code=302)
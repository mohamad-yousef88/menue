from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_settings
from app.core.database import get_db
from app.web.deps import get_current_user_from_cookie
from app.services.menu_service import MenuService
from app.schemas.menu import MenuCreate, MenuUpdate

router = APIRouter(prefix="/admin/menus", tags=["Admin Menus"])
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def list_menus(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    service = MenuService(db)
    menus = service.list_all()
    return templates.TemplateResponse(
        request=request,
        name="admin/menus.html",
        context={"user": user, "menus": menus},
    )

@router.get("/new", response_class=HTMLResponse)
def new_menu_form(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="admin/menu_form.html",
        context={"user": user, "menu": None},
    )

@router.get("/{menu_id}/edit", response_class=HTMLResponse)
def edit_menu_form(menu_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    service = MenuService(db)
    menu = service.get(menu_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/menu_form.html",
        context={"user": user, "menu": menu},
    )


@router.post("/save")
def save_menu(
    request: Request,
    menu_id: int | None = Form(None),
    name: str = Form(...),
    description: str | None = Form(None),
    is_default: bool = Form(False),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)

    service = MenuService(db)
    if menu_id:
        service.update(menu_id, MenuUpdate(
            name=name, description=description,
            is_default=is_default, is_active=is_active,
        ))
    else:
        service.create(MenuCreate(
            name=name, description=description,
            is_default=is_default, is_active=is_active,
        ))
    return RedirectResponse(url="/admin/menus", status_code=302)


@router.post("/{menu_id}/delete")
def delete_menu(menu_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)
    MenuService(db).delete(menu_id)
    return RedirectResponse(url="/admin/menus", status_code=302)
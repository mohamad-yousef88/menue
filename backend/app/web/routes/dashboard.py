from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.web.deps import get_current_user_from_cookie
from app.repositories.menu_repository import MenuRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.user_repository import UserRepository
from app.core.security import Security

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)

    menu_repo = MenuRepository(db)
    item_repo = MenuItemRepository(db)
    user_repo = UserRepository(db)

    menus = menu_repo.get_all()
    total_items = sum(item_repo.count_by_menu(m.id) for m in menus)
    total_users = user_repo.count()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "user": user,
            "total_menus": len(menus),
            "total_items": total_items,
            "total_users": total_users,
            "menus": menus[:5],
        },
    )
@router.get("/qr", response_class=HTMLResponse)
def qr_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/admin/login", status_code=302)

    # رابط صفحة الزبون
    base_url = str(request.base_url).rstrip("/")
    menu_url = f"{base_url}/menu"

    return templates.TemplateResponse(
        request=request,
        name="admin/qr.html",
        context={"user": user, "menu_url": menu_url},
    )
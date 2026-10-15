from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.menu_repository import MenuRepository
from app.repositories.menu_item_repository import MenuItemRepository

router = APIRouter(tags=["Public Pages"])
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("/menu", response_class=HTMLResponse)
def public_menu_page(
    request: Request,
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    menu_repo = MenuRepository(db)
    item_repo = MenuItemRepository(db)

    menu = menu_repo.get_visible_menu()

    items = []
    categories = []
    if menu:
        items = item_repo.get_by_menu(menu.id, category=category, only_available=True)
        categories = item_repo.get_categories(menu.id)

    return templates.TemplateResponse(
        request=request,
        name="public/menu.html",
        context={
            "menu": menu,
            "items": items,
            "categories": categories,
            "selected_category": category or "الكل",
        },
    )
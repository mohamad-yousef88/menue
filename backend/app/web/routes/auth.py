from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import Security
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/admin", tags=["Admin Auth"])
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None):
    token = request.cookies.get(Security.COOKIE_NAME)
    if token and Security.decode_token(token):
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"error": error},
    )

@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    try:
        result = service.login(LoginRequest(username=username, password=password))
    except Exception:
        return RedirectResponse(url="/admin/login?error=بيانات+غير+صحيحة", status_code=302)

    response = RedirectResponse(url="/admin", status_code=302)
    Security.set_token_cookie(response, result.access_token, result.expires_in)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    Security.delete_token_cookie(response)
    return response
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path
from app.repositories.email_repository import EmailRepository

router = APIRouter(prefix="/dashboard")
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR )

# Use the same in-memory repo as emails.py
# TODO: This should be dependency injection

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Display dashboard with email list"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


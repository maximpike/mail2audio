from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR )

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    #TODO Generate the actual OAuth URL once we have the OAuth client

    auth_url = "/auth/google/login"

    return templates.TemplateResponse(
        "landing.html", {
            "request": request,
            "auth_url": auth_url
        }
    )

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/curiosidades", response_class=HTMLResponse)
async def curiosidades(request: Request):
    return templates.TemplateResponse("curiosidades.html", {
        "request": request
    })

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.tag_repository import TagRepository
from utils.session import obtener_sesion
from typing import Optional

router = APIRouter(prefix="/tags", tags=["tags"])
templates = Jinja2Templates(directory="templates")
tag_repo = TagRepository()


@router.get("", response_class=HTMLResponse)
async def lista_tags(request: Request):
    """Muestra todas las etiquetas disponibles"""
    usuario = obtener_sesion(request)
    tags = tag_repo.get_all_tags(database)
    
    return templates.TemplateResponse("tags/lista.html", {
        "request": request,
        "usuario": usuario,
        "tags": tags
    })


@router.get("/{tag_id}", response_class=HTMLResponse)
async def carreras_por_tag(request: Request, tag_id: int):
    """Muestra todas las carreras con una etiqueta específica"""
    usuario = obtener_sesion(request)
    tag = tag_repo.get_tag_by_id(database, tag_id)
    
    if not tag:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Etiqueta no encontrada"
        })
    
    carreras = tag_repo.get_carreras_by_tag(database, tag_id)
    
    return templates.TemplateResponse("tags/carreras.html", {
        "request": request,
        "usuario": usuario,
        "tag": tag,
        "carreras": carreras
    })


# ===== RUTAS DE ADMINISTRACIÓN =====

@router.get("/admin/gestionar", response_class=HTMLResponse)
async def admin_tags(request: Request):
    """Panel de administración de etiquetas"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden acceder."
        })
    
    tags = tag_repo.get_all_tags(database)
    
    return templates.TemplateResponse("tags/admin.html", {
        "request": request,
        "usuario": usuario,
        "tags": tags
    })


@router.post("/admin/crear")
async def crear_tag(
    request: Request,
    nombre: str = Form(...),
    color: str = Form(...)
):
    """Crea una nueva etiqueta"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return RedirectResponse(url="/", status_code=303)
    
    tag_repo.crear_tag(database, nombre, color)
    return RedirectResponse(url="/tags/admin/gestionar", status_code=303)


@router.post("/admin/{tag_id}/actualizar")
async def actualizar_tag(
    request: Request,
    tag_id: int,
    nombre: str = Form(...),
    color: str = Form(...)
):
    """Actualiza una etiqueta existente"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return RedirectResponse(url="/", status_code=303)
    
    tag_repo.actualizar_tag(database, tag_id, nombre, color)
    return RedirectResponse(url="/tags/admin/gestionar", status_code=303)


@router.post("/admin/{tag_id}/eliminar")
async def eliminar_tag(request: Request, tag_id: int):
    """Elimina una etiqueta"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return RedirectResponse(url="/", status_code=303)
    
    tag_repo.eliminar_tag(database, tag_id)
    return RedirectResponse(url="/tags/admin/gestionar", status_code=303)


@router.post("/admin/carrera/{carrera_id}/agregar")
async def agregar_tag_carrera(
    request: Request,
    carrera_id: int,
    tag_id: int = Form(...)
):
    """Agrega una etiqueta a una carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return RedirectResponse(url="/", status_code=303)
    
    tag_repo.agregar_tag_a_carrera(database, carrera_id, tag_id)
    return RedirectResponse(url=f"/admin/carreras/{carrera_id}/editar", status_code=303)


@router.post("/admin/carrera/{carrera_id}/quitar/{tag_id}")
async def quitar_tag_carrera(
    request: Request,
    carrera_id: int,
    tag_id: int
):
    """Quita una etiqueta de una carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return RedirectResponse(url="/", status_code=303)
    
    tag_repo.quitar_tag_de_carrera(database, carrera_id, tag_id)
    return RedirectResponse(url=f"/admin/carreras/{carrera_id}/editar", status_code=303)

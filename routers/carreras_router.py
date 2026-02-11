from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.tag_repository import TagRepository
from utils.session import obtener_sesion
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")
tag_repo = TagRepository()

def get_carreras_from_db(search: str = None, categoria: str = None, pais: str = None):
    """Obtener carreras de la base de datos con filtros opcionales"""
    cursor = database.cursor(dictionary=True)
    
    query = "SELECT * FROM carreras WHERE 1=1"
    params = []
    
    if search:
        query += " AND (nombre LIKE %s OR pais LIKE %s OR ciudad LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)
    
    if pais:
        query += " AND pais = %s"
        params.append(pais)
    
    query += " ORDER BY nombre"
    
    cursor.execute(query, params)
    carreras = cursor.fetchall()
    cursor.close()
    return carreras

def get_carrera_by_id(carrera_id: int):
    """Obtener una carrera específica"""
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()
    cursor.close()
    return carrera

def get_comentarios_carrera(carrera_id: int):
    """Obtener comentarios de una carrera"""
    cursor = database.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, u.username 
        FROM comentarios c 
        JOIN usuarios u ON c.usuario_id = u.id 
        WHERE c.carrera_id = %s 
        ORDER BY c.created_at DESC
    """, (carrera_id,))
    comentarios = cursor.fetchall()
    cursor.close()
    return comentarios

def is_favorito(usuario_id: int, carrera_id: int):
    """Verificar si una carrera es favorita del usuario"""
    cursor = database.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM favoritos 
        WHERE usuario_id = %s AND carrera_id = %s
    """, (usuario_id, carrera_id))
    es_favorito = cursor.fetchone()[0] > 0
    cursor.close()
    return es_favorito

@router.get("/carreras", response_class=HTMLResponse)
async def lista_carreras(
    request: Request,
    search: Optional[str] = None,
    categoria: Optional[str] = None,
    pais: Optional[str] = None
):
    usuario = obtener_sesion(request)
    carreras = get_carreras_from_db(search, categoria, pais)
    
    # Obtener categorías y países únicos para filtros
    cursor = database.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM carreras ORDER BY categoria")
    categorias = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT pais FROM carreras ORDER BY pais")
    paises = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return templates.TemplateResponse("carreras/lista.html", {
        "request": request,
        "usuario": usuario,
        "carreras": carreras,
        "categorias": categorias,
        "paises": paises,
        "search": search,
        "categoria_filtro": categoria,
        "pais_filtro": pais
    })

@router.get("/carreras/{carrera_id}", response_class=HTMLResponse)
async def detalle_carrera(request: Request, carrera_id: int):
    usuario = obtener_sesion(request)
    carrera = get_carrera_by_id(carrera_id)
    
    if not carrera:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Carrera no encontrada"
        })
    
    comentarios = get_comentarios_carrera(carrera_id)
    es_favorito = False
    
    if usuario:
        es_favorito = is_favorito(usuario['user_id'], carrera_id)
    
    # Obtener tags de la carrera
    tags = tag_repo.get_tags_by_carrera(database, carrera_id)
    
    # Calcular valoración promedio
    valoracion_promedio = 0
    if comentarios:
        total = sum(c['valoracion'] for c in comentarios)
        valoracion_promedio = round(total / len(comentarios), 1)
    
    return templates.TemplateResponse("carreras/detalle.html", {
        "request": request,
        "usuario": usuario,
        "carrera": carrera,
        "comentarios": comentarios,
        "es_favorito": es_favorito,
        "tags": tags,
        "valoracion_promedio": valoracion_promedio
    })

@router.post("/carreras/{carrera_id}/favorito")
async def toggle_favorito(request: Request, carrera_id: int):
    usuario = obtener_sesion(request)
    
    if not usuario:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    cursor = database.cursor()
    
    # Verificar si ya es favorito
    cursor.execute("""
        SELECT id FROM favoritos 
        WHERE usuario_id = %s AND carrera_id = %s
    """, (usuario['user_id'], carrera_id))
    
    if cursor.fetchone():
        # Si existe, eliminar
        cursor.execute("""
            DELETE FROM favoritos 
            WHERE usuario_id = %s AND carrera_id = %s
        """, (usuario['user_id'], carrera_id))
    else:
        # Si no existe, agregar
        cursor.execute("""
            INSERT INTO favoritos (usuario_id, carrera_id) 
            VALUES (%s, %s)
        """, (usuario['user_id'], carrera_id))
    
    database.commit()
    cursor.close()
    
    return RedirectResponse(url=f"/carreras/{carrera_id}", status_code=303)

@router.post("/carreras/{carrera_id}/comentario")
async def agregar_comentario(
    request: Request,
    carrera_id: int,
    comentario: str = Form(...),
    valoracion: int = Form(...)
):
    usuario = obtener_sesion(request)
    
    if not usuario:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    cursor = database.cursor()
    cursor.execute("""
        INSERT INTO comentarios (usuario_id, carrera_id, comentario, valoracion)
        VALUES (%s, %s, %s, %s)
    """, (usuario['user_id'], carrera_id, comentario, valoracion))
    database.commit()
    cursor.close()
    
    return RedirectResponse(url=f"/carreras/{carrera_id}", status_code=303)

@router.get("/mis-favoritos", response_class=HTMLResponse)
async def mis_favoritos(request: Request):
    usuario = obtener_sesion(request)
    
    if not usuario:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    cursor = database.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.* FROM carreras c
        JOIN favoritos f ON c.id = f.carrera_id
        WHERE f.usuario_id = %s
        ORDER BY f.created_at DESC
    """, (usuario['user_id'],))
    favoritos = cursor.fetchall()
    cursor.close()
    
    return templates.TemplateResponse("carreras/favoritos.html", {
        "request": request,
        "usuario": usuario,
        "favoritos": favoritos
    })

# ===== RUTAS DE ADMINISTRACIÓN =====

@router.get("/admin/carreras", response_class=HTMLResponse)
async def admin_carreras(request: Request):
    """Panel de administración de carreras"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden acceder."
        })
    
    carreras = get_carreras_from_db()
    
    return templates.TemplateResponse("admin/carreras_admin.html", {
        "request": request,
        "usuario": usuario,
        "carreras": carreras
    })

@router.get("/admin/carreras/nueva", response_class=HTMLResponse)
async def nueva_carrera_form(request: Request):
    """Formulario para crear nueva carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden crear carreras."
        })
    
    return templates.TemplateResponse("admin/carrera_form.html", {
        "request": request,
        "usuario": usuario,
        "carrera": None,
        "accion": "Crear"
    })

@router.post("/admin/carreras/nueva")
async def crear_carrera(
    request: Request,
    nombre: str = Form(...),
    pais: str = Form(...),
    ciudad: str = Form(...),
    categoria: str = Form(...),
    longitud_km: float = Form(...),
    descripcion: str = Form(...)
):
    """Crear nueva carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado."
        })
    
    cursor = database.cursor()
    cursor.execute("""
        INSERT INTO carreras (nombre, pais, ciudad, categoria, longitud_circuito, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, pais, ciudad, categoria, longitud_km, descripcion))
    database.commit()
    cursor.close()
    
    return RedirectResponse(url="/admin/carreras", status_code=303)

@router.get("/admin/carreras/{carrera_id}/editar", response_class=HTMLResponse)
async def editar_carrera_form(request: Request, carrera_id: int):
    """Formulario para editar carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado."
        })
    
    carrera = get_carrera_by_id(carrera_id)
    
    if not carrera:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Carrera no encontrada"
        })
    
    # Obtener tags de la carrera y todos los tags disponibles
    carrera_tags = tag_repo.get_tags_by_carrera(database, carrera_id)
    todos_tags = tag_repo.get_all_tags(database)
    
    return templates.TemplateResponse("admin/carrera_form.html", {
        "request": request,
        "usuario": usuario,
        "carrera": carrera,
        "carrera_tags": carrera_tags,
        "todos_tags": todos_tags,
        "accion": "Editar"
    })

@router.post("/admin/carreras/{carrera_id}/editar")
async def actualizar_carrera(
    request: Request,
    carrera_id: int,
    nombre: str = Form(...),
    pais: str = Form(...),
    ciudad: str = Form(...),
    categoria: str = Form(...),
    longitud_km: float = Form(...),
    descripcion: str = Form(...)
):
    """Actualizar carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado."
        })
    
    cursor = database.cursor()
    cursor.execute("""
        UPDATE carreras 
        SET nombre = %s, pais = %s, ciudad = %s, categoria = %s, 
            longitud_circuito = %s, descripcion = %s
        WHERE id = %s
    """, (nombre, pais, ciudad, categoria, longitud_km, descripcion, carrera_id))
    database.commit()
    cursor.close()
    
    return RedirectResponse(url="/admin/carreras", status_code=303)

@router.post("/admin/carreras/{carrera_id}/eliminar")
async def eliminar_carrera(request: Request, carrera_id: int):
    """Eliminar carrera"""
    usuario = obtener_sesion(request)
    
    if not usuario or not usuario.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado."
        })
    
    cursor = database.cursor()
    # Eliminar comentarios y favoritos relacionados primero
    cursor.execute("DELETE FROM comentarios WHERE carrera_id = %s", (carrera_id,))
    cursor.execute("DELETE FROM favoritos WHERE carrera_id = %s", (carrera_id,))
    cursor.execute("DELETE FROM carreras WHERE id = %s", (carrera_id,))
    database.commit()
    cursor.close()
    
    return RedirectResponse(url="/admin/carreras", status_code=303)


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from utils.session import obtener_sesion
from datetime import datetime, timedelta

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/calendario", response_class=HTMLResponse)
async def calendario(request: Request):
    usuario = obtener_sesion(request)
    
    cursor = database.cursor(dictionary=True)
    
    # Obtener eventos próximos (desde hoy)
    hoy = datetime.now().date()
    cursor.execute("""
        SELECT ce.*, c.nombre as carrera_nombre, c.pais, c.categoria
        FROM calendario_eventos ce
        JOIN carreras c ON ce.carrera_id = c.id
        WHERE ce.fecha_evento >= %s
        ORDER BY ce.fecha_evento ASC, ce.hora_evento ASC
        LIMIT 20
    """, (hoy,))
    eventos_proximos = cursor.fetchall()
    
    # Obtener eventos pasados recientes
    cursor.execute("""
        SELECT ce.*, c.nombre as carrera_nombre, c.pais, c.categoria
        FROM calendario_eventos ce
        JOIN carreras c ON ce.carrera_id = c.id
        WHERE ce.fecha_evento < %s
        ORDER BY ce.fecha_evento DESC, ce.hora_evento DESC
        LIMIT 10
    """, (hoy,))
    eventos_pasados = cursor.fetchall()
    
    cursor.close()
    
    # Calcular cuenta regresiva para el próximo evento
    proximo_evento = eventos_proximos[0] if eventos_proximos else None
    cuenta_regresiva = None
    
    if proximo_evento:
        fecha_evento = proximo_evento['fecha_evento']
        if isinstance(fecha_evento, str):
            fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%d').date()
        dias_restantes = (fecha_evento - hoy).days
        cuenta_regresiva = dias_restantes
    
    return templates.TemplateResponse("calendario.html", {
        "request": request,
        "usuario": usuario,
        "eventos_proximos": eventos_proximos,
        "eventos_pasados": eventos_pasados,
        "proximo_evento": proximo_evento,
        "cuenta_regresiva": cuenta_regresiva
    })

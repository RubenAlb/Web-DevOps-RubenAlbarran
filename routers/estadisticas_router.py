from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from utils.session import obtener_sesion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/estadisticas", response_class=HTMLResponse)
async def estadisticas(request: Request):
    usuario = obtener_sesion(request)
    
    cursor = database.cursor(dictionary=True)
    
    # Total de carreras
    cursor.execute("SELECT COUNT(*) as total FROM carreras")
    total_carreras = cursor.fetchone()['total']
    
    # Carreras por categoría
    cursor.execute("""
        SELECT categoria, COUNT(*) as total 
        FROM carreras 
        GROUP BY categoria 
        ORDER BY total DESC
    """)
    carreras_por_categoria = cursor.fetchall()
    
    # Carreras por país (Top 10)
    cursor.execute("""
        SELECT pais, COUNT(*) as total 
        FROM carreras 
        GROUP BY pais 
        ORDER BY total DESC 
        LIMIT 10
    """)
    carreras_por_pais = cursor.fetchall()
    
    # Total de usuarios
    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']
    
    # Total de comentarios
    cursor.execute("SELECT COUNT(*) as total FROM comentarios")
    total_comentarios = cursor.fetchone()['total']
    
    # Valoración promedio global
    cursor.execute("SELECT AVG(valoracion) as promedio FROM comentarios")
    valoracion_promedio = cursor.fetchone()['promedio']
    if valoracion_promedio:
        valoracion_promedio = round(float(valoracion_promedio), 1)
    else:
        valoracion_promedio = 0
    
    # Carreras más comentadas
    cursor.execute("""
        SELECT c.nombre, c.pais, COUNT(co.id) as total_comentarios
        FROM carreras c
        LEFT JOIN comentarios co ON c.id = co.carrera_id
        GROUP BY c.id
        ORDER BY total_comentarios DESC
        LIMIT 5
    """)
    carreras_mas_comentadas = cursor.fetchall()
    
    # Carreras mejor valoradas
    cursor.execute("""
        SELECT c.nombre, c.pais, AVG(co.valoracion) as valoracion_promedio,
               COUNT(co.id) as total_valoraciones
        FROM carreras c
        INNER JOIN comentarios co ON c.id = co.carrera_id
        GROUP BY c.id
        HAVING COUNT(co.id) >= 1
        ORDER BY valoracion_promedio DESC, total_valoraciones DESC
        LIMIT 5
    """)
    carreras_mejor_valoradas = cursor.fetchall()
    
    # Total de favoritos
    cursor.execute("SELECT COUNT(*) as total FROM favoritos")
    total_favoritos = cursor.fetchone()['total']
    
    cursor.close()
    
    return templates.TemplateResponse("estadisticas.html", {
        "request": request,
        "usuario": usuario,
        "total_carreras": total_carreras,
        "total_usuarios": total_usuarios,
        "total_comentarios": total_comentarios,
        "total_favoritos": total_favoritos,
        "valoracion_promedio": valoracion_promedio,
        "carreras_por_categoria": carreras_por_categoria,
        "carreras_por_pais": carreras_por_pais,
        "carreras_mas_comentadas": carreras_mas_comentadas,
        "carreras_mejor_valoradas": carreras_mejor_valoradas
    })

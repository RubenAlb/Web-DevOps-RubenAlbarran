from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from data.database import database
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["API"])

@router.get("/carreras")
async def get_carreras_api(
    search: Optional[str] = None,
    categoria: Optional[str] = None,
    pais: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """Obtener listado de carreras en formato JSON"""
    cursor = database.cursor(dictionary=True)
    
    query = "SELECT * FROM carreras WHERE 1=1"
    params = []
    
    if search:
        query += " AND (nombre LIKE %s OR pais LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param])
    
    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)
    
    if pais:
        query += " AND pais = %s"
        params.append(pais)
    
    query += f" ORDER BY nombre LIMIT {limit} OFFSET {offset}"
    
    cursor.execute(query, params)
    carreras = cursor.fetchall()
    cursor.close()
    
    return {"success": True, "data": carreras, "count": len(carreras)}

@router.get("/carreras/{carrera_id}")
async def get_carrera_api(carrera_id: int):
    """Obtener detalle de una carrera específica"""
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carreras WHERE id = %s", (carrera_id,))
    carrera = cursor.fetchone()
    cursor.close()
    
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    return {"success": True, "data": carrera}

@router.get("/carreras/{carrera_id}/comentarios")
async def get_comentarios_api(carrera_id: int):
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
    
    return {"success": True, "data": comentarios, "count": len(comentarios)}

@router.get("/calendario")
async def get_eventos_api(limit: int = 20):
    """Obtener eventos del calendario"""
    from datetime import datetime
    cursor = database.cursor(dictionary=True)
    
    hoy = datetime.now().date()
    cursor.execute("""
        SELECT ce.*, c.nombre as carrera_nombre, c.pais, c.categoria
        FROM calendario_eventos ce
        JOIN carreras c ON ce.carrera_id = c.id
        WHERE ce.fecha_evento >= %s
        ORDER BY ce.fecha_evento ASC
        LIMIT %s
    """, (hoy, limit))
    eventos = cursor.fetchall()
    cursor.close()
    
    return {"success": True, "data": eventos, "count": len(eventos)}

@router.get("/estadisticas")
async def get_estadisticas_api():
    """Obtener estadísticas generales del sistema"""
    cursor = database.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM carreras")
    total_carreras = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM comentarios")
    total_comentarios = cursor.fetchone()['total']
    
    cursor.execute("SELECT AVG(valoracion) as promedio FROM comentarios")
    valoracion_promedio = cursor.fetchone()['promedio']
    if valoracion_promedio:
        valoracion_promedio = round(float(valoracion_promedio), 1)
    else:
        valoracion_promedio = 0
    
    cursor.execute("""
        SELECT categoria, COUNT(*) as total 
        FROM carreras 
        GROUP BY categoria 
        ORDER BY total DESC
    """)
    carreras_por_categoria = cursor.fetchall()
    
    cursor.close()
    
    return {
        "success": True,
        "data": {
            "total_carreras": total_carreras,
            "total_usuarios": total_usuarios,
            "total_comentarios": total_comentarios,
            "valoracion_promedio": valoracion_promedio,
            "carreras_por_categoria": carreras_por_categoria
        }
    }

@router.get("/paises")
async def get_paises_api():
    """Obtener lista de países únicos"""
    cursor = database.cursor()
    cursor.execute("SELECT DISTINCT pais FROM carreras ORDER BY pais")
    paises = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return {"success": True, "data": paises, "count": len(paises)}

@router.get("/categorias")
async def get_categorias_api():
    """Obtener lista de categorías únicas"""
    cursor = database.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM carreras ORDER BY categoria")
    categorias = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return {"success": True, "data": categorias, "count": len(categorias)}

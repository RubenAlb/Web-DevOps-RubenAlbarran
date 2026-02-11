from typing import Annotated
from fastapi import FastAPI, Request,Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from data.database import database
from data.carrerita_repository import CarreritaRepository
from domain.model.Carrerita import Carrerita
from starlette.middleware.sessions import SessionMiddleware
from routers.juego_router import juego_router
from routers.auth_router import router as auth_router
from routers.carreras_router import router as carreras_router
from routers.paises_router import router as paises_router
from routers.curiosidades_router import router as curiosidades_router
from routers.calendario_router import router as calendario_router
from routers.estadisticas_router import router as estadisticas_router
from routers.api_router import router as api_router
from routers.tags_router import router as tags_router
from utils.session import obtener_sesion

import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(title="Mi Primera Web FastAPI", description="Ejemplo básico con Jinja2")

# Evento de inicio: Inicializar las tablas de la base de datos
@app.on_event("startup")
async def startup_event():
    """Inicializar la base de datos al arrancar la aplicación"""
    try:
        cursor = database.cursor()
        
        # Crear tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Verificar si ya existe el usuario admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO usuarios (username, password, email) VALUES 
                ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oo1qWv3OqWa2', 'admin@example.com')
            """)
            print("✓ Usuario admin creado (username: admin, password: admin123)")
        
        # Crear tabla de carreritas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carreritas (
                id VARCHAR(10) PRIMARY KEY,
                nombre_carrera VARCHAR(100) NOT NULL
            )
        """)
        
        # Crear tabla de juegos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS juegos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                puntuacion INT NOT NULL,
                intentos INT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        
        # Crear tabla de carreras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carreras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                pais VARCHAR(100) NOT NULL,
                ciudad VARCHAR(100) NOT NULL,
                descripcion TEXT,
                descripcion_corta VARCHAR(500),
                fecha VARCHAR(50),
                categoria VARCHAR(100),
                longitud_circuito DECIMAL(10,3),
                numero_vueltas INT,
                record_vuelta VARCHAR(50),
                total_curvas INT,
                historia TEXT,
                primera_edicion VARCHAR(50),
                campeon_mas_exitoso VARCHAR(200),
                victorias_record INT,
                asistencia_record INT,
                imagen_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de favoritos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favoritos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                carrera_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
                UNIQUE KEY unique_favorito (usuario_id, carrera_id)
            )
        """)
        
        # Crear tabla de comentarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                carrera_id INT NOT NULL,
                comentario TEXT NOT NULL,
                valoracion INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
            )
        """)
        
        # Crear tabla de calendario de eventos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calendario_eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                carrera_id INT NOT NULL,
                fecha_evento DATE NOT NULL,
                hora_evento TIME,
                tipo_evento VARCHAR(50) NOT NULL,
                descripcion VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
            )
        """)
        
        # Crear tabla de curiosidades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS curiosidades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(200) NOT NULL,
                descripcion TEXT NOT NULL,
                icono VARCHAR(50),
                categoria VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        database.commit()
        cursor.close()
        print("✓ Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"⚠ Error al inicializar la base de datos: {e}")

# Cámbiala clave secreta en producción
app.add_middleware(
    SessionMiddleware,
    secret_key="tu_clave_secreta_muy_segura_cambiala_en_produccion",
    session_cookie="session",
    max_age=3600 * 24 * 7,  # 7 días
    same_site="lax",
    https_only=False  # Cambiar a True en producción con HTTPS
)

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")

# Configurar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir el router de autenticación
app.include_router(auth_router)

# Incluir los nuevos routers
app.include_router(carreras_router)
app.include_router(paises_router)
app.include_router(curiosidades_router)
app.include_router(calendario_router)
app.include_router(estadisticas_router)
app.include_router(api_router)
app.include_router(tags_router)



#RUTA RAIZ
@app.get("/")
async def inicio(request: Request):
    """Página de inicio"""
    sesion = obtener_sesion(request)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "usuario": sesion
    })

@app.get("/api-docs")
async def api_documentation(request: Request):
    """Documentación de la API REST"""
    sesion = obtener_sesion(request)
    return templates.TemplateResponse("api_docs.html", {
        "request": request,
        "usuario": sesion
    })



# ======================== RUTAS PARA CARRERITAS ========================

# Ver todas las carreritas
@app.get("/carreritas", response_class=HTMLResponse)
async def carreritas(request: Request):
    """Listar todas las carreritas"""
    carreritas_repo = CarreritaRepository()
    carreritas = carreritas_repo.get_all(database)
    return templates.TemplateResponse("carreritas.html", {
        "request": request,
        "carreritas": carreritas
    })

# Formulario para insertar carrerita
@app.get("/insert_carrerita", response_class=HTMLResponse)
async def insert_carrerita(request: Request):
    """Formulario para insertar una nueva carrerita"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden insertar carreritas."
        })
    return templates.TemplateResponse("insert_carrerita.html", {"request": request})

# Procesar inserción de carrerita
@app.post("/do_insertar_carrerita")
async def do_insertar_carrerita(request: Request,
                                id: Annotated[str, Form()],
                                nombre_carrera: Annotated[str, Form()]):
    """Insertar una nueva carrerita en la base de datos"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden insertar carreritas."
        })
    carreritas_repo = CarreritaRepository()
    carrerita = Carrerita(id, nombre_carrera)
    carreritas_repo.insertar_carrerita(database, carrerita)
    return templates.TemplateResponse("do_insert_carrerita.html", {"request": request})


# Formulario para actualizar carrerita
@app.get("/actualizar_carrerita", response_class=HTMLResponse)
async def actualizar_carrerita(request: Request, id: Optional[str] = None):
    """Formulario para actualizar una carrerita"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden actualizar carreritas."
        })
    carreritas_repo = CarreritaRepository()
    
    if id:
        carrerita = carreritas_repo.get_by_id(database, id)
        return templates.TemplateResponse("actualizar_carrerita.html", {
            "request": request,
            "carrerita": carrerita
        })
    else:
        carreritas = carreritas_repo.get_all(database)
        return templates.TemplateResponse("actualizar_carrerita.html", {
            "request": request,
            "carreritas": carreritas
        })


# Procesar actualización de carrerita
@app.post("/do_actualizar_carrerita")
async def do_actualizar_carrerita(request: Request,
                                  id: Annotated[str, Form()],
                                  nombre_carrera: Annotated[str, Form()]):
    """Actualizar una carrerita en la base de datos"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden actualizar carreritas."
        })
    carreritas_repo = CarreritaRepository()
    carrerita = Carrerita(id, nombre_carrera)
    carreritas_repo.actualizar_carrerita(database, carrerita)
    return templates.TemplateResponse("do_actualizar_carrerita.html", {"request": request})


# Lista para borrar carrerita
@app.get("/borrar_carrerita", response_class=HTMLResponse)
async def borrar_carrerita(request: Request):
    """Lista de carreritas para borrar"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden borrar carreritas."
        })
    carreritas_repo = CarreritaRepository()
    carreritas = carreritas_repo.get_all(database)
    return templates.TemplateResponse("borrar_carrerita.html", {
        "request": request,
        "carreritas": carreritas
    })


# Procesar borrado de carrerita
@app.post("/do_borrar_carrerita")
async def do_borrar_carrerita(request: Request,
                              id: Annotated[str, Form()]):
    """Borrar una carrerita de la base de datos"""
    sesion = obtener_sesion(request)
    if not sesion or not sesion.get('is_admin'):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "Acceso denegado. Solo los administradores pueden borrar carreritas."
        })
    carreritas_repo = CarreritaRepository()
    carreritas_repo.borrar_carrerita(database, id)
    return templates.TemplateResponse("do_borrar_carrerita.html", {"request": request})


# ======================== FIN RUTAS CARRERITAS ========================


# Página de juegos
@app.get("/juegos", response_class=HTMLResponse)
async def juegos(request: Request):
    """Página de juegos"""
    return templates.TemplateResponse("juegos.html", {"request": request})


# Incluir el router de juegos
app.include_router(juego_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.usuario_repository import UsuarioRepository
from utils.session import crear_sesion, destruir_sesion

# Crear el router
router = APIRouter(prefix="/auth", tags=["auth"])

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Muestra el formulario de login"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def do_login(request: Request,
                   username: Annotated[str, Form()],
                   password: Annotated[str, Form()]):
    """Procesa el login"""
    try:
        usuario_repo = UsuarioRepository()
        usuario = usuario_repo.get_by_username(database, username)
        
        if usuario and usuario_repo.verificar_password(password, usuario.password):
            crear_sesion(request, usuario.id, usuario.username, usuario.is_admin)
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Usuario o contraseña incorrectos"
            })
    except Exception as e:
        print(f"ERROR EN LOGIN: {str(e)}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"Error en el sistema: {str(e)}"
        })


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """Muestra el formulario de registro"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def do_register(request: Request,
                      username: Annotated[str, Form()],
                      email: Annotated[str, Form()],
                      password: Annotated[str, Form()],
                      password_confirm: Annotated[str, Form()]):
    """Procesa el registro de nuevo usuario"""
    if password != password_confirm:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Las contraseñas no coinciden"
        })
    
    usuario_repo = UsuarioRepository()
    
    # Verificar si el usuario ya existe
    if usuario_repo.get_by_username(database, username):
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "El usuario ya existe"
        })
    
    # Crear el usuario
    try:
        usuario = usuario_repo.crear_usuario(database, username, password, email)
        crear_sesion(request, usuario.id, usuario.username, usuario.is_admin)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": f"Error al crear el usuario: {str(e)}"
        })


@router.get("/logout")
async def logout(request: Request):
    """Cierra la sesión del usuario"""
    destruir_sesion(request)
    return RedirectResponse(url="/", status_code=303)

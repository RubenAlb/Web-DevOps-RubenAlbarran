from typing import Annotated
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Crear el router
juego_router = APIRouter(prefix="/juego", tags=["juego"])

# Configurar las plantillas
templates = Jinja2Templates(directory="templates")


def reiniciar_juego(request: Request):
    """Reinicia el juego con valores por defecto"""
    import random
    request.session["numero_aleatorio"] = random.randint(1, 100)
    request.session["numero_intentos"] = 0


@juego_router.get("/", response_class=HTMLResponse)
async def mostrar_juego(request: Request,
                       numero: str = None):
    return templates.TemplateResponse("juego.html", {"request": request})


@juego_router.post("/", response_class=HTMLResponse)
async def mostrar_juego(request: Request,
                       numero: Annotated[str, Form()] = None):
    # la primera vez que se accede no existe la variable de sesión
    if "numero_intentos" not in request.session:
        reiniciar_juego(request)
    
    # las siguientes veces
    request.session["numero_intentos"] += 1
    if (request.session["numero_intentos"] > 10):
        mensaje = "¡Has superado el número máximo de intentos!"
    
    elif (int(numero) < request.session["numero_aleatorio"]):
        mensaje = f"El número es mayor, te quedan {10 - request.session['numero_intentos']} intentos"
    
    elif (int(numero) > request.session["numero_aleatorio"]):
        mensaje = f"El número es menor, te quedan {10 - request.session['numero_intentos']} intentos"
    
    else:
        mensaje = f"¡Felicidades! Has acertado el número en {request.session['numero_intentos']} intentos"
        reiniciar_juego(request)
    
    return templates.TemplateResponse("juego.html", {
        "request": request,
        "mensaje": mensaje
    })


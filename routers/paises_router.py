from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Datos de ejemplo para países
paises_datos = [
    {
        "id": 1,
        "nombre": "Italia",
        "bandera": "🇮🇹",
        "continente": "Europa",
        "total_carreras": "2",
        "total_circuitos": "3",
        "carreras_destacadas": "Monza, Imola",
        "primera_carrera_año": "1921",
        "campeones_locales": "15",
        "victorias_totales": "95",
        "asistencia_promedio": "200,000",
        "descripcion": "Italia es la cuna del automovilismo deportivo. Casa de Ferrari, el país ha celebrado carreras desde los inicios del deporte. El Gran Premio de Italia en Monza es una de las carreras más antiguas y emocionantes del calendario de F1, conocida por su atmósfera apasionada y sus fanáticos tifosi.",
        "carreras": [
            {
                "id": 1,
                "nombre": "Gran Premio de Italia (Monza)",
                "descripcion_corta": "El templo de la velocidad, con la afición más apasionada de F1"
            },
            {
                "id": 2,
                "nombre": "Gran Premio de Emilia-Romagna (Imola)",
                "descripcion_corta": "Circuito histórico que rinde homenaje a Ayrton Senna"
            }
        ],
        "datos_curiosos": [
            {"icono": "🏎️", "titulo": "Ferrari", "descripcion": "Casa de la escudería más legendaria de F1"},
            {"icono": "🏁", "titulo": "Monza Magic", "descripcion": "El circuito más rápido del calendario"},
            {"icono": "❤️", "titulo": "Tifosi", "descripcion": "Los fans más apasionados del automovilismo"}
        ]
    },
    {
        "id": 2,
        "nombre": "Reino Unido",
        "bandera": "🇬🇧",
        "continente": "Europa",
        "total_carreras": "2",
        "total_circuitos": "5",
        "carreras_destacadas": "Silverstone, Brands Hatch",
        "primera_carrera_año": "1926",
        "campeones_locales": "20",
        "victorias_totales": "110",
        "asistencia_promedio": "150,000",
        "descripcion": "El Reino Unido es considerado el hogar espiritual de la Fórmula 1, con la mayoría de los equipos basados aquí. Silverstone fue la sede de la primera carrera del campeonato mundial en 1950 y sigue siendo una de las carreras más importantes del año.",
        "carreras": [
            {
                "id": 3,
                "nombre": "Gran Premio de Gran Bretaña (Silverstone)",
                "descripcion_corta": "La carrera que inició el campeonato mundial de F1"
            }
        ],
        "datos_curiosos": [
            {"icono": "🏆", "titulo": "Origen de F1", "descripcion": "Primera carrera del campeonato mundial"},
            {"icono": "🏭", "titulo": "Valle de Velocidad", "descripcion": "7 de 10 equipos de F1 tienen sede aquí"},
            {"icono": "🎓", "titulo": "Ingeniería", "descripcion": "Centro mundial de ingeniería de motorsport"}
        ]
    },
    {
        "id": 3,
        "nombre": "Mónaco",
        "bandera": "🇲🇨",
        "continente": "Europa",
        "total_carreras": "1",
        "total_circuitos": "1",
        "carreras_destacadas": "Gran Premio de Mónaco",
        "primera_carrera_año": "1929",
        "campeones_locales": "1",
        "victorias_totales": "32",
        "asistencia_promedio": "200,000",
        "descripcion": "Mónaco es sinónimo de glamour y prestigio en el mundo de las carreras. A pesar de ser el país más pequeño con una carrera de F1, su Gran Premio es considerado el más prestigioso y difícil del calendario.",
        "carreras": [
            {
                "id": 1,
                "nombre": "Gran Premio de Mónaco",
                "descripcion_corta": "La joya de la corona de la Fórmula 1"
            }
        ],
        "datos_curiosos": [
            {"icono": "💎", "titulo": "Glamour", "descripcion": "La carrera más prestigiosa y glamurosa"},
            {"icono": "🚢", "titulo": "Yates", "descripcion": "Vista única desde yates en el puerto"},
            {"icono": "👑", "titulo": "Triple Corona", "descripcion": "Parte de la Triple Corona del Automovilismo"}
        ]
    },
    {
        "id": 4,
        "nombre": "Japón",
        "bandera": "🇯🇵",
        "continente": "Asia",
        "total_carreras": "1",
        "total_circuitos": "3",
        "carreras_destacadas": "Suzuka",
        "primera_carrera_año": "1976",
        "campeones_locales": "0",
        "victorias_totales": "48",
        "asistencia_promedio": "120,000",
        "descripcion": "Japón ha sido un pilar fundamental en la F1 moderna, especialmente durante la era de los motores Honda. Suzuka es considerado uno de los circuitos más técnicos y desafiantes del calendario.",
        "carreras": [
            {
                "id": 4,
                "nombre": "Gran Premio de Japón (Suzuka)",
                "descripcion_corta": "Figura en ocho, uno de los circuitos más técnicos"
            }
        ],
        "datos_curiosos": [
            {"icono": "🎌", "titulo": "Figura 8", "descripcion": "Único circuito en forma de ocho"},
            {"icono": "🏎️", "titulo": "Honda", "descripcion": "Casa de uno de los fabricantes más exitosos"},
            {"icono": "🎯", "titulo": "Precisión", "descripcion": "Requiere máxima precisión en cada curva"}
        ]
    }
]

@router.get("/paises", response_class=HTMLResponse)
async def lista_paises(request: Request):
    return templates.TemplateResponse("paises/lista.html", {
        "request": request,
        "paises": paises_datos
    })

@router.get("/paises/{pais_id}", response_class=HTMLResponse)
async def detalle_pais(request: Request, pais_id: int):
    pais = next((p for p in paises_datos if p["id"] == pais_id), None)
    if not pais:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": "País no encontrado"
        })
    return templates.TemplateResponse("paises/detalle.html", {
        "request": request,
        "pais": pais
    })

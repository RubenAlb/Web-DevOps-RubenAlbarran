# CI/CD Pipeline - FastAPI Carreras

## 🚀 Pipeline Automatizado

Este proyecto incluye un pipeline completo de CI/CD usando GitHub Actions.

### 📋 Workflows Configurados

#### 1. **CI/CD Principal** (`.github/workflows/ci-cd.yml`)

Se ejecuta en cada push y pull request a las ramas `main` y `develop`.

**Jobs incluidos:**
- ✅ **Test y Verificación**
  - Instalación de dependencias
  - Verificación de formato con Black
  - Análisis de código con Flake8
  - Ejecución de tests con pytest
  - Verificación de importación del módulo principal

- 🏗️ **Build y Validación**
  - Verificación de estructura del proyecto
  - Validación de archivos requeridos

- 🔒 **Análisis de Seguridad**
  - Verificación de vulnerabilidades con Safety
  - Análisis de seguridad con Bandit
  - Generación de reportes de seguridad

- 📦 **Información de Despliegue**
  - Preparación de información para despliegue
  - Comandos de despliegue manual
  - Instrucciones para Docker

#### 2. **Docker Build & Deploy** (`.github/workflows/deploy-docker.yml`)

Se ejecuta en:
- Push a la rama `main`
- Creación de tags con formato `v*`
- Manualmente via workflow_dispatch

**Funcionalidades:**
- 🐳 Construcción de imagen Docker
- 📤 Push a GitHub Container Registry
- 🏷️ Gestión automática de tags

### 🔧 Archivos de Configuración

#### `Dockerfile`
Imagen Docker optimizada para producción:
- Base: Python 3.11-slim
- Puerto: 8000
- Comando: `uvicorn main:app --host 0.0.0.0 --port 8000`

#### `.dockerignore`
Optimiza el contexto de construcción de Docker excluyendo archivos innecesarios.

#### `.gitignore`
Previene el commit de archivos temporales, caché, y configuraciones locales.

### 📝 Tests

Archivo `test_main.py` con tests básicos:
- ✅ Verificación del endpoint principal
- ✅ Existencia de la aplicación
- ✅ Carga de routers
- ✅ Existencia de directorios requeridos
- ✅ Validación de requirements.txt

### 🎯 Badges (Agregar al README principal)

```markdown
![CI/CD](https://github.com/RubenAlb/Web-DevOps-RubenAlbarran/actions/workflows/ci-cd.yml/badge.svg)
![Docker Build](https://github.com/RubenAlb/Web-DevOps-RubenAlbarran/actions/workflows/deploy-docker.yml/badge.svg)
```

### 💻 Ejecución Local

#### Instalar dependencias de desarrollo
```bash
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black safety bandit
```

#### Ejecutar tests
```bash
pytest -v
pytest --cov=. --cov-report=html
```

#### Verificar formato de código
```bash
black --check .
flake8 .
```

#### Verificar seguridad
```bash
safety check
bandit -r . -f screen
```

### 🐳 Docker

#### Construir imagen
```bash
docker build -t fastapi-carreras .
```

#### Ejecutar contenedor
```bash
docker run -p 8000:8000 fastapi-carreras
```

#### Usar docker-compose (opcional)
Crear archivo `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./static:/app/static
      - ./templates:/app/templates
```

### 📊 Monitoreo del Pipeline

1. Ve a la pestaña **Actions** en GitHub
2. Observa el estado de los workflows
3. Revisa los logs de cada job
4. Descarga los artefactos generados (reportes de seguridad)

### 🔄 Flujo de Trabajo Recomendado

1. **Desarrollo Local**
   - Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
   - Hacer cambios y commits
   - Ejecutar tests localmente: `pytest`
   - Verificar formato: `black .`

2. **Push y PR**
   - Push a GitHub: `git push origin feature/nueva-funcionalidad`
   - Crear Pull Request a `develop`
   - El CI/CD se ejecuta automáticamente
   - Revisar resultados del pipeline

3. **Merge a Main**
   - Merge de `develop` a `main`
   - Se ejecuta el pipeline completo + Docker build
   - Imagen disponible en GitHub Container Registry

### 🎓 Mejoras Futuras

- [ ] Despliegue automático a producción (Heroku, AWS, Azure, etc.)
- [ ] Tests de integración con base de datos
- [ ] Tests end-to-end con Selenium
- [ ] Métricas de cobertura de código
- [ ] Análisis de rendimiento
- [ ] Notificaciones (Slack, Discord, Email)
- [ ] Ambientes de staging
- [ ] Rollback automático en caso de fallo

### 📚 Recursos

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Docs](https://docs.docker.com/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Autor:** Ruben Albarran  
**Proyecto:** Web+DevOps  
**Fecha:** Febrero 2026

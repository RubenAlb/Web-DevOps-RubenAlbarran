"""
Tests básicos para la aplicación FastAPI
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    """Test del endpoint principal"""
    response = client.get("/")
    assert response.status_code == 200


def test_app_exists():
    """Verificar que la aplicación existe"""
    assert app is not None
    assert app.title == "Mi Primera Web FastAPI"


def test_routers_loaded():
    """Verificar que los routers están cargados"""
    routes = [route.path for route in app.routes]
    assert len(routes) > 0
    print(f"Rutas cargadas: {len(routes)}")


def test_templates_directory():
    """Verificar que el directorio de templates existe"""
    import os
    assert os.path.exists("templates")
    assert os.path.isdir("templates")


def test_static_directory():
    """Verificar que el directorio static existe"""
    import os
    assert os.path.exists("static")
    assert os.path.isdir("static")


def test_requirements_file():
    """Verificar que requirements.txt existe y tiene contenido"""
    import os
    assert os.path.exists("requirements.txt")
    with open("requirements.txt", "r") as f:
        content = f.read()
        assert "fastapi" in content.lower()
        assert "uvicorn" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

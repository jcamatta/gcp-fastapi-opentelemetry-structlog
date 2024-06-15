from src.main import app
from fastapi.testclient import TestClient

# Es un objeto que permite realizar request http: GET | POST | etc.
# Recibe una app con los endpoints que buscamos testear.
# Lo que hacemos es pegarle a los endpoints con una data test y chequear el response esperado.
client = TestClient(app=app)

def test_app_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"working": True}
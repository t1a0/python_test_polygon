from fastapi.testclient import TestClient
from ingredient_service import app as ingredient_app

ingredient_client = TestClient(ingredient_app)

def test_add_invalid_ingredient():
    response = ingredient_client.post("/add_ingredient/yeast/1")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data

def test_add_ingredient():
    response = ingredient_client.post("/add_ingredient/flour/2")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_get_ingredients():
    response = ingredient_client.get("/get_ingredients")
    assert response.status_code == 200
    data = response.json()
    assert "flour" in data
    assert "water" in data
    assert "sugar" in data
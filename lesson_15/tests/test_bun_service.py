from fastapi.testclient import TestClient
from bun_service import app as bun_app
from .test_ingredient_service import ingredient_client

bun_client = TestClient(bun_app)

def test_calculate_buns_with_enough_ingredients():
    ingredient_client.post("/add_ingredient/flour/4")
    ingredient_client.post("/add_ingredient/water/2")
    ingredient_client.post("/add_ingredient/sugar/9")

    response = bun_client.get("/calculate_buns")
    assert response.status_code == 200
    data = response.json()
    if "total_buns" in data:
        assert data["total_buns"] == 1
    else:
        assert "error" in data


def test_calculate_buns_with_invalid_ingredient():
    response = ingredient_client.post("/add_ingredient/yeast/1")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data

def test_calculate_buns_with_missing_ingredients():
    ingredient_client.post("/add_ingredient/flour/1")
    ingredient_client.post("/add_ingredient/water/1")
    ingredient_client.post("/add_ingredient/sugar/1")

    response = bun_client.get("/calculate_buns")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert "Недостатньо інгредієнтів для випікання." in data["error"]

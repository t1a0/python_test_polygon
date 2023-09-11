from fastapi import FastAPI
import httpx

app = FastAPI()


async def get_ingredient_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/get_ingredients")
        return response.json()


async def calculate_buns():
    ingredient_data = await get_ingredient_data()
    flour = ingredient_data.get("flour", 0)
    water = ingredient_data.get("water", 0)
    sugar = ingredient_data.get("sugar", 0)

    if flour >= 2 and water >= 1 and sugar >= 3:
        num_buns = min(flour // 2, water, sugar // 3)
        return {"total_buns": num_buns}
    else:
        return {"error": "Недостатньо інгредієнтів для випікання."}



@app.get("/calculate_buns")
async def get_calculate_buns():
    return await calculate_buns()

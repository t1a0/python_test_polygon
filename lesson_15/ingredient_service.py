from fastapi import FastAPI

app = FastAPI()
ingredients = {
    "flour": 0,
    "water": 0,
    "sugar": 0,
}


@app.post("/add_ingredient/{name}/{quantity}")
async def add_ingredient(name: str, quantity: int):
    if name in ingredients:
        ingredients[name] += quantity
        return {"message": f"Додано {quantity}  {name}."}
    else:
        return {"error": f"Інгредієнт {name} не використовується у рецептурі."}


@app.get("/get_ingredients")
async def get_ingredients():
    return ingredients

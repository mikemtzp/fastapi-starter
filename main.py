from fastapi import FastAPI

from routers import models, products, users

app = FastAPI()

# Start server: uvicorn main:app --reload

# Routers
app.include_router(models.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World from Fast API!"}

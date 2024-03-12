from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import models, products, users

app = FastAPI()

# Start server: uvicorn main:app --reload

# Routers
app.include_router(models.router)
app.include_router(products.router)
app.include_router(users.router)

# Access image at: http://127.0.0.1:8000/snow/images/gothic-snowflake.jpeg
app.mount("/snow", StaticFiles(directory="static"), name="snow")

@app.get("/")
async def root():
    return {"message": "Hello World from Fast API!"}

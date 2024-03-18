from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import basic_auth_users, jwt_auth_user, models, products, users, users_db_local

app = FastAPI()

# Start server: uvicorn main:app --reload

# Routers
app.include_router(models.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_user.router)

# Remote DB

# Local DB
# app.include_router(users_db_local.router)

# Access image at: http://127.0.0.1:8000/snow/images/gothic-snowflake.jpeg
app.mount("/snow", StaticFiles(directory="static"), name="snow")


@app.get("/")
async def root():
    return {"message": "Hello World from Fast API!"}

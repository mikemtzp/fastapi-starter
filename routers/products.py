from fastapi import APIRouter

router = APIRouter(tags=["products"])

products_list = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]


@router.get("/products")
async def products():
    return products_list


@router.get("/product/{id}")
async def products(id: int):
    return products_list[id]

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="Patrick", surname="Galante", url="https://i9k.dev", age=32),
    User(
        id=2, name="Courtney", surname="LaPlante", url="https://spiritbox.com", age=35
    ),
    User(id=3, name="Brian", surname="Garris", url="https://kloose.com", age=30),
]


@router.get("/usersjson")
async def users():
    return [
        {
            "name": "Patrick",
            "surname": "Galante",
            "url": "https://i9k.dev",
            "age": 32,
        },
        {
            "name": "Courtney",
            "surname": "LaPlante",
            "url": "https://spiritbox.com",
            "age": 35,
        },
        {
            "name": "Brian",
            "surname": "Garris",
            "url": "https://kloose.com",
            "age": 30,
        },
    ]


@router.get("/users", response_model=list[User])
async def users():
    return users_list


@router.get("/user/{id}", response_model=User)  # Path
async def user(id: int):
    return search_user(id)


@router.get("/user", response_model=User)  # Query
async def user(id: int):
    return search_user(id)


@router.post("/user", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(
            status_code=409, detail=f"User with id: {user.id} already exists"
        )

    users_list.routerend(user)
    return user


@router.put("/user", response_model=User)
async def user(user: User):

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user

    raise HTTPException(status_code=404, detail=f"User with id: {user.id} not found.")


@router.delete("/user/{id}")
async def delete_user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"detail": f"User with id: {id} has been successfully deleted."}

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found.")


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail=f"User with id: {id} not found.")

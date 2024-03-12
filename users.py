from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


@app.get("/usersjson")
async def get_users():
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


@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}")  # Path
async def user(id: int):
    return search_user(id)


@app.get("/user")  # Query
async def user(id: int):
    return search_user(id)


@app.post("/user")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "User already exists"}

    users_list.append(user)
    return user


@app.put("/user")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "Fail to update user"}

    return user


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}

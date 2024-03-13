from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mike": {
        "username": "mike",
        "full_name": "Mike Martinez",
        "email": "mike@dev.com",
        "disabled": False,
        "password": "123456",
    },
    "spencer": {
        "username": "spencer",
        "full_name": "Spencer Charnas",
        "email": "spencer@i9k.com",
        "disabled": True,
        "password": "98765",
    },
}

def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])

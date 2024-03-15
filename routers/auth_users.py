from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class BearerToken(BaseModel):
    access_token: str
    token_type: str

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


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unactive user",
        )

    return user


@app.post("/login", response_model=BearerToken)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid user")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Wrong password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user

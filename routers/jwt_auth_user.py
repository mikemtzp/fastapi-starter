from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# To generate a secure random secret key use the command: openssl rand -hex 32
SECRET_KEY = "16671074f6684e65a0887bc29e6464b893d069a1ae87eb2ac7909f5026d83909"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


class Token(BaseModel):
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
        "password": "$2a$12$lP4P4WjZ8MADNU9R6BYmgeQI3cSFtgRhGJp5cXQmOlFgIYxeB93qS",
    },
    "spencer": {
        "username": "spencer",
        "full_name": "Spencer Charnas",
        "email": "spencer@i9k.com",
        "disabled": True,
        "password": "$2a$12$ZemSlAw0h4re8d1BV8yyN.lukMAVMIKRUAiIllSzb8CezDTd.Hd3.",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unactive user",
        )

    return user


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid user")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    access_token = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/users/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user

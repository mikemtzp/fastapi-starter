from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from db.models.user import User
from db.remote_client import client
from db.schemas.user import user_schema, users_schema

router = APIRouter(
    tags=["usersdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "User not found"}},
)

# Assigment: client.<database>.<collection>
users_db = client.test.users


@router.get("/usersdb", response_model=list[User])
async def users():
    return users_schema(users_db.find())


@router.get("/userdb/{id}", response_model=User)
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/userdb", response_model=User)
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/userdb", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists",
        )

    user_dict = dict(user)
    del user_dict["id"]

    id = users_db.insert_one(user_dict).inserted_id

    new_user = user_schema(users_db.find_one({"_id": id}))

    return User(**new_user)


@router.put("/userdb", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        users_db.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "Could not update user."}

    return search_user("_id", ObjectId(user.id))


@router.delete("/userdb/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = users_db.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "Could not delete user"}


def search_user(field: str, value):
    try:
        user = users_db.find_one({field: value})
        return User(**user_schema(user))
    except:
        return {"error": "User not found."}

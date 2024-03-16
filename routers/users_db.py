from fastapi import APIRouter, HTTPException, status

from db.models.user import User
from db.client import db_client

router = APIRouter(
    tags=["usersdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "User not found"}},
)


users_list = []


@router.get("/usersdb", response_model=list[User])
async def users():
    return users_list


@router.get("/userdb/{id}", response_model=User)
async def user(id: int):
    return search_user(id)


@router.get("/userdb", response_model=User)
async def user(id: int):
    return search_user(id)


@router.post("/userdb", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"User with id: {user.id} already exists",
    #     )

    db_client.local
    return user


@router.put("/userdb", response_model=User)
async def user(user: User):

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user

    raise HTTPException(status_code=404, detail=f"User with id: {user.id} not found.")


@router.delete("/userdb/{id}")
async def delete_user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"detail": f"User with id: {id} has been successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found."
    )


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found.",
        )

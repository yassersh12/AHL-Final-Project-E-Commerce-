from fastapi import APIRouter, HTTPException, Depends, status
from app.models import User
from app.api.services.user_service import UserService
from typing import List

router = APIRouter()
user_service = UserService()


@router.post("/users", response_model=User)
def create_user(user: User):
    return user_service.create_user(user)


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[User])
def get_all_users():
    return user_service.get_all_users()


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, updated_user: User):
    user = user_service.update_user(user_id, updated_user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: str):
    user = user_service.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

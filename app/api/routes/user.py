from fastapi import APIRouter, HTTPException, Depends, status
from app.models import User
from app.api.services.user_service import UserService
from typing import List
from app.api.dependencies.password_utils import validate_password
from passlib.context import CryptContext
from app.models import UserDTO


router = APIRouter()
user_service = UserService()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users", response_model=UserDTO)
def create_user(user: User):

    validate_password(user.hashed_password)
    user.hashed_password = pwd_context.hash(user.hashed_password)
    created_user = user_service.create_user(user)
    return UserDTO.from_orm(created_user)


@router.get("/users/{user_id}", response_model=UserDTO)
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.from_orm(user)


@router.get("/users", response_model=List[UserDTO])
def get_all_users():
    users = user_service.get_all_users()
    return [UserDTO.from_orm(user) for user in users]


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

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from app.api.services.user_service import UserService
from app.api.exceptions.global_exceptions import (
    InvalidPasswordException,
    EmailAlreadyExistsException,
    UserNotFoundException,
    InvalidUUIDException,
)
from uuid import UUID
from app.api.dependencies.auth import *

router = APIRouter()


# this method for normal user
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    user_dict = user.model_dump()
    user_dict["is_admin"] = False
    return service.create_user(UserCreateRequest(**user_dict))


# this method only for admins to regiter users
def create_user(
    user: UserCreateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin),
):
    service = UserService(db)
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise InvalidUUIDException()

    service = UserService(db)
    try:
        return service.get_user(user_uuid)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_data: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise InvalidUUIDException()

    service = UserService(db)
    return service.update_user(user_uuid, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise InvalidUUIDException()

    service = UserService(db)
    try:
        service.delete_user(user_uuid)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin),
):
    service = UserService(db)
    return service.get_all_users()

from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from app.db import database
from app.api.dependencies.password_utils import validate_password
from app.api.exceptions.GlobalException import (
    InvalidPasswordException,
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from fastapi import HTTPException
from app.models import UserDTO, UserResponse, UserUpdateDTO
import logging
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        if self.db.query(User).filter(User.email == user.email).first():
            raise EmailAlreadyExistsException()
        validate_password(user.password)
        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user(self, user_id: UUID):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
        except ValueError:
            raise UserNotFoundException()

        if not user:
            raise UserNotFoundException()
        return user

    def update_user(self, user_id: UUID, user_data: UserUpdateDTO):
        user = self.get_user(user_id)

        if user_data.username is not None:
            user.username = user_data.username

        if user_data.password:
            validate_password(user_data.password)
            user.hashed_password = pwd_context.hash(user_data.password)

        self.db.commit()
        self.db.refresh(user)
        return UserResponse.from_orm(user)

    def delete_user(self, user_id: UUID):
        user = self.get_user(user_id)

        if user:
            self.db.delete(user)
            self.db.commit()
            return user
        raise UserNotFoundException()

    def get_all_users(self):
        return self.db.query(User).all()

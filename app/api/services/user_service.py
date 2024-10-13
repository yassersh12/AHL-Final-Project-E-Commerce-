from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from passlib.context import CryptContext
from app.db import database
from app.api.dependencies.password_utils import validate_password
from app.api.exceptions.global_exceptions import (
    InvalidPasswordException,
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreateRequest):
        if self.db.query(User).filter(User.email == user.email).first():
            raise EmailAlreadyExistsException()

        validate_password(user.password)

        hashed_password = pwd_context.hash(user.password)

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def get_user(self, user_id: UUID):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException()
        return user

    def update_user(self, user_id: UUID, user_data: UserUpdateRequest):
        user = self.get_user(user_id)

        if user_data.username is not None:
            user.username = user_data.username

        if user_data.password:
            validate_password(user_data.password)
            user.hashed_password = pwd_context.hash(user_data.password)

        if user_data.email is not None:
            existing_user = (
                self.db.query(User).filter(User.email == user_data.email).first()
            )
            if existing_user and existing_user.id != user.id:
                raise EmailAlreadyExistsException()

            user.email = user_data.email

        user.updated_at = datetime.utcnow()
        self.db.commit()
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

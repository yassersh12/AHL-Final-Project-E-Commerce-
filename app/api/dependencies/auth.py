from datetime import datetime, timedelta, timezone
from typing import Annotated
from app.models import *
import jwt
from app.api.dependencies.password_utils import *
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# this is a fake DB, I will remove it when adding the real DB
user_db = {
    "johndoe": {
        "username": "yasser",
        "full_name": "yassersharabati",
        "email": "yassersh@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "active": False,
    }
}


def get_user(db, username: str):
    try:
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)
    except Exception as e:
        print(f"An error occurred while getting user: {e}")
        return None


def authenticate_user(username: str, password: str):
    try:
        user = get_user(user_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"An error occurred while creating access token: {e}")
        return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        print(f"An error occurred while decoding token: {e}")
        raise credentials_exception
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        if not current_user.active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    except Exception as e:
        print(f"An error occurred while getting current active user: {e}")
        raise HTTPException(status_code=400, detail="Error getting current active user")


async def get_current_active_admin(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
        )
    return current_user

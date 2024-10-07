from uuid import uuid4, UUID
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from decimal import Decimal
from datetime import datetime


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID !  ")
    name: str = Field(..., description="Product Name !  ")
    description: str = Field(None, description="Product Description ! ")
    price: Decimal = Field(..., description="Product Price !  ", gt=0)
    stock: Optional[int] = Field(None, description="Stock Quantity ", ge=0)
    isAvailable: bool = Field(default=True, description="Is Product Available ? ")


class User(BaseModel):
    id: Optional[UUID] = Field(
        None, description="User ID. Automatically generated upon user creation."
    )
    username: str = Field(..., description="User Name.")
    email: EmailStr = Field(..., description="The email address of the user.")
    hashed_password: str = Field(..., description="The Password of the user.")
    is_admin: bool = Field(False, description="Admin or not?")
    is_active: bool = Field(True, description="User active or not?")
    created_at: Optional[datetime] = Field(
        None, description="The date and time when the user was created."
    )
    updated_at: Optional[datetime] = Field(
        None, description="The date and time when the user was last updated."
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: UUID | None = None


class UserDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
        from_attributes = True

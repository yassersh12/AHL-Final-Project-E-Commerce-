from uuid import uuid4, UUID
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.api.exceptions.GlobalException import (
    PriceValidationException,
    StockValidationException,
)


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID !  ")
    name: str = Field(..., description="Product Name !  ")
    description: str = Field(None, description="Product Description ! ")
    price: Decimal = Field(..., description="Product Price !  ")
    stock: Optional[int] = Field(None, description="Stock Quantity ")
    isAvailable: bool = Field(default=True, description="Is Product Available ? ")

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise PriceValidationException()
        return value

    @validator("stock")
    def validate_stock(cls, value):
        if value is not None and value < 0:
            raise StockValidationException()
        return value


class User(BaseModel):
    id: Optional[UUID] = Field(None, description="User ID Automatically Created . !  ")
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
    id: Optional[UUID] = Field(
        None, description="User ID. Automatically generated upon user creation."
    )
    username: str = Field(..., description="User Name.")
    email: EmailStr = Field(..., description="The email address of the user.")
    is_admin: bool = Field(False, description="Admin or not?")
    is_active: bool = Field(True, description="User active or not?")
    created_at: Optional[datetime] = Field(
        None, description="The date and time when the user was created."
    )
    updated_at: Optional[datetime] = Field(
        None, description="The date and time when the user was last updated."
    )

    class Config:
        orm_mode = True
        from_attributes = True

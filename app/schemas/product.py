from pydantic import BaseModel, Field, condecimal, constr
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ProductCreate(BaseModel):
    name: str = Field(None)
    description: str = Field(None)
    price: float = Field(None)
    stock: int = Field(None)
    is_available: bool = Field(None)

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
        orm_mode = True
        arbitrary_types_allowed = True


class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    is_available: bool
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        from_attributes = True
        orm_mode = True
        arbitrary_types_allowed = True


class ProductUpdate(BaseModel):
    name: str = Field(None)
    description: str = Field(None)
    price: float = Field(None)
    stock: int = Field(None)
    is_available: bool = Field(None)

    class Config:
        from_attributes = True
        orm_mode = True
        arbitrary_types_allowed = True


class ProductSearchParams(BaseModel):
    name: Optional[str] = Field(
        default=None, description="Partial or full product name"
    )
    min_price: Optional[Decimal] = Field(default=None, description="Minimum price")
    max_price: Optional[Decimal] = Field(default=None, description="Maximum price")
    isAvailable: Optional[bool] = Field(
        default=None, description="Filter by availability"
    )
    page: int = Field(default=1, ge=1, description="Page number for pagination")
    page_size: int = Field(
        default=20, ge=1, le=100, description="Number of products per page"
    )
    sort_by: str = Field(default="name", description="Sort by field")
    sort_order: str = Field(default="asc", description="Sort order: asc or desc")

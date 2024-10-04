from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID !  ")
    name: str = Field(..., description="Product Name !  ")
    description: str = Field(None, description="Product Description ! ")
    price: Decimal = Field(..., description="Product Price !  ", gt=0)
    stock: Optional[int] = Field(None, description="Stock Quantity ", ge=0)
    isAvailable: bool = Field(default=True, description="Is Product Available ? ")

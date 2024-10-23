from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class OrderItem(BaseModel):
    product_id: UUID = Field(..., description="Product ID connected to the order.")
    quantity: int = Field(..., description="Quantity of the product in the order.")

class OrderResponse(BaseModel):
    id: UUID = Field(..., description="Order ID.")
    user_id: Optional[UUID] = Field(None, description="User ID connected to the order.")
    status: str = Field(..., description="Status of the order.")  # e.g., "pending"
    total_price: Decimal = Field(..., description="Total price of the order.", gt=0, max_digits=10, decimal_places=2)
    created_at: datetime = Field(..., description="Time the order was created.")
    updated_at: Optional[datetime] = Field(None, description="Time of the last update for the order.")
    products: List[OrderProductResponse] = Field(..., description="List of products in the order.")

class OrderCreationResponse(BaseModel):
    id: UUID = Field(..., description="Order ID.")
    user_id: Optional[UUID] = Field(None, description="User ID connected to the order.")
    status: str = Field(..., description="Status of the order.")  
    total_price: Decimal = Field(..., description="Total price of the order.", gt=0, max_digits=10, decimal_places=2)
    created_at: datetime = Field(..., description="Time the order was created.")

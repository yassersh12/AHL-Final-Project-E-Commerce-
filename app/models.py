from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.database import Base
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TokenData(BaseModel):
    username: UUID | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(User):
    hashed_password: str

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
class Order(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4(), description="Order ID.")
    user_id: Optional[UUID] = Field(None, description="User ID connected to a user.") # references user, SET NULL on delete, on database implementation
    status_id: Optional[UUID] = Field(None, description="Status ID connected to an order_status.") # references order_status, SET NULL on delete, on database implementation
    total_price: Decimal = Field(..., description="Total price of the order.", gt=0, max_digits=10, decimal_places=2)
    created_at: datetime = Field(datetime.now, description="Time the order is created at.")
    updated_at: datetime = Field(None, description="Time of the last update for the order.")

class OrderProductResponse(BaseModel):
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

class OrderStatus(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4(), description="order_status ID.")
    name: str = Field("pending", description="Name of the order_status.", unique=True)
    created_at: datetime = Field(datetime.now, description="Time the order_status is created at.")
    updated_at: datetime = Field(None, description="Time of the last update for the order_status.")

class OrderProduct(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4(), description="order_product ID.")
    order_id: Optional[UUID] = Field(None, description="Order ID connected to an order.") # references order, CASCADE on delete, on database implementation
    product_id: Optional[UUID] = Field(None, description="Product ID connected to an Product.") # references product, SET NULL on delete, on database implementation
    quantity: int = Field(..., description="Quantity of order_products.")
    created_at: datetime = Field(datetime.now, description="Time the order_product is created at.")
    updated_at: datetime = Field(None, description="Time of the last update for the order_product.")

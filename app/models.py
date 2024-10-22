from typing import List, Optional
from sqlalchemy import Column, ForeignKey, DECIMAL, DateTime, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
from app.db.database import Base
from pydantic import BaseModel
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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("order_status.id", ondelete="SET NULL"), nullable=True
    )
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    status: Mapped["OrderStatus"] = relationship("OrderStatus", back_populates="orders")
    products: Mapped[List["OrderProduct"]] = relationship(
        "OrderProduct", back_populates="order", cascade="all, delete-orphan"
    )


class OrderProduct(Base):
    __tablename__ = "order_products"



class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)

    order: Mapped["Order"] = relationship("Order", back_populates="products")
    product: Mapped["Product"] = relationship("Product", back_populates="order_products")


class OrderStatus(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid.uuid4(), description="order_status ID.")
    name: str = Field("pending", description="Name of the order_status.", unique=True)
    created_at: datetime = Field(datetime.now, description="Time the order_status is created at.")
    updated_at: datetime = Field(None, description="Time of the last update for the order_status.")


    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

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

class OrderStatus(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4(), description="order_status ID.")
    name: str = Field("pending", description="Name of the order_status.", unique=True)
    created_at: datetime = Field(datetime.now, description="Time the order_status is created at.")
    updated_at: datetime = Field(None, description="Time of the last update for the order_status.")
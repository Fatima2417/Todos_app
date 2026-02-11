from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
import uuid


class UserBase(SQLModel):
    email: str = Field(sa_column_kwargs={"unique": True, "index": True})
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.
    """
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    hashed_password: str = Field()

    conversations: List["Conversation"] = Relationship(back_populates="user")


class UserRead(SQLModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserCreate(SQLModel):
    email: str
    password: str  # We'll use this to create hashed_password
    first_name: Optional[str] = None
    last_name: Optional[str] = None
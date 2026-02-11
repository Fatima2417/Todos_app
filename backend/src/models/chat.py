from typing import List, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: Optional["User"] = Relationship(back_populates="conversations")

class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[List[dict]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
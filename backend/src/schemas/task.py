from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Schema for validating new task creation requests."""
    title: str = Field(..., min_length=1, max_length=200, description="The task title")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed task description")


class TaskUpdate(BaseModel):
    """Schema for validating task update requests."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated task title")
    description: Optional[str] = Field(None, max_length=1000, description="Updated task description")
    completed: Optional[bool] = Field(None, description="Updated completion status")


class TaskPublic(BaseModel):
    """Schema for serializing task responses for external consumption."""
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enables ORM to Pydantic conversion
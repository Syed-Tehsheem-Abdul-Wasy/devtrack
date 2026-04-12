from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    project_id: int = Field(foreign_key="project.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    priority: str = Field(default="medium")
    status: str = Field(default="todo")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
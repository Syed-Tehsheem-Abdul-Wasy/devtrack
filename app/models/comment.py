from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    author_id: int = Field(foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

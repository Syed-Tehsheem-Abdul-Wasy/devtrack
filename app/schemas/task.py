from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"
    status: str = "todo"
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None

class TaskRead(BaseModel):
    id: int
    title: str
    project_id: int
    assignee_id: Optional[int] = None
    priority: str
    status: str
    created_at: datetime

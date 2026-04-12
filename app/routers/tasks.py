from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.comment import Comment
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.schemas.comment import CommentCreate, CommentRead
from app.core.dependencies import get_current_user

router = APIRouter(tags=["Tasks"])

@router.post("/projects/{project_id}/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, task_in: TaskCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
    task = Task(**task_in.model_dump(), project_id=project_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/projects/{project_id}/tasks/", response_model=List[TaskRead])
def list_tasks(project_id: int, status: Optional[str] = None, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    query = select(Task).where(Task.project_id == project_id)
    if status is not None:
        query = query.where(Task.status == status)
        
    tasks = session.exec(query).all()
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    project = session.get(Project, task.project_id)
    if task.assignee_id != current_user.id and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    project = session.get(Project, task.project_id)
    if project.owner_id != current_user.id and task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        
    session.delete(task)
    session.commit()
    return None

@router.post("/tasks/{task_id}/comments/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(task_id: int, comment_in: CommentCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    comment = Comment(**comment_in.model_dump(), task_id=task_id, author_id=current_user.id)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router.get("/tasks/{task_id}/comments/", response_model=List[CommentRead])
def list_comments(task_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    comments = session.exec(select(Comment).where(Comment.task_id == task_id)).all()
    return comments

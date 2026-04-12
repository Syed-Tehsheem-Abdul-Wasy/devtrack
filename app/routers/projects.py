from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = Project(**project_in.model_dump(), owner_id=current_user.id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/", response_model=List[ProjectRead])
def list_projects(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Fetch projects where the user is the owner
    owned_projects = session.exec(select(Project).where(Project.owner_id == current_user.id)).all()
    
    # Fetch projects where the user is an assignee on a task
    tasks = session.exec(select(Task).where(Task.assignee_id == current_user.id)).all()
    member_project_ids = [task.project_id for task in tasks]
    
    if member_project_ids:
        member_projects = session.exec(select(Project).where(Project.id.in_(member_project_ids))).all()
    else:
        member_projects = []
        
    all_projects = {p.id: p for p in owned_projects + member_projects}
    return list(all_projects.values())

@router.get("/{id}", response_model=ProjectRead)
def get_project(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.put("/{id}", response_model=ProjectRead)
def update_project(id: int, project_update: ProjectUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    session.delete(project)
    session.commit()
    return None

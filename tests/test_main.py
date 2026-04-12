import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import uuid

from app.main import app
from app.database import get_session

# Use in-memory SQLite for testing
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_register(client: TestClient):
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": unique_email,
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert "id" in data

def test_login(client: TestClient):
    unique_email = f"test_login_{uuid.uuid4()}@example.com"
    client.post("/auth/register", json={
        "name": "Test User",
        "email": unique_email,
        "password": "password123"
    })
    
    response = client.post("/auth/login", data={
        "username": unique_email,
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_project(client: TestClient):
    unique_email = f"test_project_{uuid.uuid4()}@example.com"
    client.post("/auth/register", json={
        "name": "Project User",
        "email": unique_email,
        "password": "password123"
    })
    
    login_resp = client.post("/auth/login", data={
        "username": unique_email,
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/projects/", json={
        "name": "New Project",
        "description": "Project Description"
    }, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Project"
    assert "id" in data

def test_create_task(client: TestClient):
    unique_email = f"test_task_{uuid.uuid4()}@example.com"
    client.post("/auth/register", json={
        "name": "Task User",
        "email": unique_email,
        "password": "password123"
    })
    
    login_resp = client.post("/auth/login", data={
        "username": unique_email,
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    project_resp = client.post("/projects/", json={
        "name": "Task Project",
        "description": "Project Description"
    }, headers=headers)
    
    project_id = project_resp.json()["id"]
    
    task_resp = client.post(f"/projects/{project_id}/tasks/", json={
        "title": "First Task",
        "priority": "high",
        "status": "todo"
    }, headers=headers)
    
    assert task_resp.status_code == 201
    data = task_resp.json()
    assert data["title"] == "First Task"
    assert data["project_id"] == project_id

def test_create_comment(client: TestClient):
    unique_email = f"test_comment_{uuid.uuid4()}@example.com"
    client.post("/auth/register", json={
        "name": "Comment User",
        "email": unique_email,
        "password": "password123"
    })
    
    login_resp = client.post("/auth/login", data={
        "username": unique_email,
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    project_resp = client.post("/projects/", json={
        "name": "Comment Project",
        "description": "Project Description"
    }, headers=headers)
    project_id = project_resp.json()["id"]
    
    task_resp = client.post(f"/projects/{project_id}/tasks/", json={
        "title": "Task for Comment",
        "priority": "high",
        "status": "todo"
    }, headers=headers)
    task_id = task_resp.json()["id"]
    
    comment_resp = client.post(f"/tasks/{task_id}/comments/", json={
        "content": "This is a comment"
    }, headers=headers)
    
    assert comment_resp.status_code == 201
    data = comment_resp.json()
    assert data["content"] == "This is a comment"
    assert data["task_id"] == task_id

---
name: backend-skill
description: Build robust FastAPI backends. Create RESTful routes, handle HTTP requests/responses, implement business logic, integrate with databases, and enforce security patterns.
---

# Backend Development Skill

## Core Responsibilities

1.  **FastAPI Application & Route Management**: Structure the main application, create API routers, and define RESTful endpoints with proper HTTP methods.
2.  **Request/Response Handling**: Validate incoming data with Pydantic models and serialize outgoing data, ensuring clear contracts between frontend and backend.
3.  **Dependency Injection & Security**: Implement FastAPI's `Depends` to manage authentication, database sessions, and other cross-cutting concerns cleanly.
4.  **Business Logic Orchestration**: Write the service-layer code that contains the core rules of your application, acting as the mediator between API routes and the data layer.
5.  **Database Integration**: Coordinate with the Database Agent to execute CRUD operations, ensuring all data access is secure and user-scoped.
6.  **Error Handling & Validation**: Define clear HTTP exception responses for client and server errors, and validate business rules.

## Instructions

### 1. Application and Router Structure

Organize your backend into a clear module structure. Use FastAPI's `APIRouter` to group related endpoints.

```python
# File: src/main.py (Application Entry Point)
from fastapi import FastAPI
from .routers import tasks, auth  # Import your routers

app = FastAPI(title="Todo API", version="1.0")

# Include routers with prefixes and tags
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}
```

```python
# File: src/routers/tasks.py (Task-specific Router)
from fastapi import APIRouter, Depends, HTTPException
from typing import List
# Import your schemas, services, and dependencies
from ..schemas import task as task_schemas
from ..services import task_service
from ..dependencies import get_current_user

router = APIRouter()

# All endpoints in this router will require authentication
# The `get_current_user` dependency validates the JWT token.
@router.get("/tasks", response_model=List[task_schemas.TaskPublic])
def list_user_tasks(
    completed: Optional[bool] = None,  # Query parameter for filtering
    current_user = Depends(get_current_user),
    db = Depends(get_db_session)
):
    """List all tasks for the current user, with optional filtering."""
    tasks = task_service.get_tasks_for_user(
        db=db,
        user_id=current_user.id,
        completed_filter=completed
    )
    return tasks
```

### 2. Defining Schemas (Request/Response Validation)

Use Pydantic models to define the exact shape of data coming in and going out of your API.

```python
# File: src/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema for creating a task (what the API expects from a POST request)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

# Schema for returning a task (what the API sends in a response)
class TaskPublic(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    # Don't expose sensitive internal fields like `user_id` unless necessary

    class Config:
        from_attributes = True  # Allows conversion from ORM objects (SQLModel)
```

### 3. Implementing Secure Endpoints with Dependencies

Create endpoints that are protected by authentication. Use dependencies to inject the current user and database session.

```python
# File: src/routers/tasks.py (continued)
@router.post("/tasks", response_model=task_schemas.TaskPublic)
def create_task(
    task_in: task_schemas.TaskCreate,
    current_user = Depends(get_current_user),  # Injects the validated user
    db = Depends(get_db_session)  # Injects a database session
):
    """
    Create a new task for the currently authenticated user.
    """
    # Delegate the business logic to a service function
    new_task = task_service.create_task_for_user(
        db=db,
        task_data=task_in,
        user_id=current_user.id  # CRITICAL: Pass the user's ID
    )
    return new_task

@router.get("/tasks", response_model=List[task_schemas.TaskPublic])
def list_user_tasks(
    completed: Optional[bool] = None,  # Query parameter for filtering
    current_user = Depends(get_current_user),
    db = Depends(get_db_session)
):
    """List all tasks for the current user, with optional filtering."""
    tasks = task_service.get_tasks_for_user(
        db=db,
        user_id=current_user.id,
        completed_filter=completed
    )
    return tasks
```

### 4. Service Layer (Business Logic)

This layer contains your application's rules and acts as a bridge between the API and the database.

```python
# File: src/services/task_service.py
from sqlmodel import Session, select
from .. import models
from ..schemas import task as task_schemas

def create_task_for_user(db: Session, task_data: task_schemas.TaskCreate, user_id: str):
    """Business logic for creating a task."""
    # 1. Create the database model instance
    db_task = models.Task(**task_data.dict(), user_id=user_id)

    # 2. Persist it (this is where you would collaborate with the Database Agent)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # 3. Return the result
    return db_task

def get_tasks_for_user(db: Session, user_id: str, completed_filter: bool = None):
    """Business logic for retrieving a user's tasks."""
    statement = select(models.Task).where(models.Task.user_id == user_id)  # SECURITY: Filter by user

    if completed_filter is not None:
        statement = statement.where(models.Task.completed == completed_filter)

    tasks = db.exec(statement).all()
    return tasks
```

### 5. Dependency for Authentication & Database

```python
# File: src/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import get_db_session  # Function to get a DB session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db_session)
):
    """Dependency to validate JWT token and return the current user."""
    token = credentials.credentials
    # Call a function (likely provided by the Auth Agent) to validate the token
    user_id = validate_jwt_and_get_user_id(token)  # This function needs to be implemented
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    # You might fetch the full user object from the DB here
    return {"id": user_id}
```

## Best Practices

### Security & Data Integrity
- Never Trust the Client: Re-validate all inputs in the backend, even if validated on the frontend. The user_id must always come from the validated JWT token (current_user.id), never from a client-supplied URL parameter.
- Use response_model: This ensures your API's output matches the documented schema and filters out any unexpected data from your database models.
- HTTPS Only: Enforce HTTPS in production.

### Code Structure
- Thin Controllers, Fat Services: Keep your route functions (controllers) thin. They should primarily handle HTTP-related tasks and delegate business logic to service functions.
- Explicit Imports: Avoid circular dependencies by having a clear import structure (e.g., schemas don't import models).
- Meaningful HTTP Status Codes: Return 201 Created for successful POSTs, 404 Not Found for missing resources, 403 Forbidden for authorization failures.

### Performance
- Use Database Indexes: Ensure the Database Agent creates indexes on user_id and other frequently filtered columns.
- Session Management: Keep database sessions short. Open them at the start of a request and close them at the end using dependencies.

### Common Endpoint Pattern

```python
# GET /api/tasks/{task_id}
@router.get("/tasks/{task_id}", response_model=task_schemas.TaskPublic)
def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db_session)
):
    db_task = task_service.get_task_by_id_for_user(db, task_id, current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Check that the task belongs to the current user (service layer should do this)
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return db_task
```
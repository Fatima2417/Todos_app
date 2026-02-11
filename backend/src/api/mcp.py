from fastmcp import FastMCP
from ..auth.jwt import verify_token
from ..database.engine import engine
from ..models.task import Task
from sqlmodel import Session, select
from datetime import datetime, timezone

# T009: Initialize FastMCP server instance
mcp = FastMCP("TodoAssistant")

# T008: Implement JWT validation utility
def validate_token_and_get_user(jwt_token: str) -> str:
    """
    Validates the JWT token and returns the user_id (sub).
    This ensures that every tool call is authenticated.
    """
    try:
        payload = verify_token(jwt_token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing 'sub' claim")
        return user_id
    except Exception as e:
        raise ValueError(f"Authentication failed: {str(e)}")

# LOGIC FUNCTIONS (Callable internally)

def add_task(jwt_token: str, title: str, description: str = None):
    """Add a new task. Requires a valid JWT token."""
    user_id = validate_token_and_get_user(jwt_token)
    
    with Session(engine) as session:
        new_task = Task(
            title=title,
            description=description,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return f"Successfully added task: {new_task.title} (ID: {new_task.id})"

def list_tasks(jwt_token: str):
    """List all pending tasks. Requires a valid JWT token."""
    user_id = validate_token_and_get_user(jwt_token)
    
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id, Task.completed == False)
        tasks = session.exec(statement).all()
        if not tasks:
            return "You have no pending tasks."
        
        result = "Your pending tasks:\n"
        for i, task in enumerate(tasks, 1):
            result += f"{i}. {task.title} (ID: {task.id})\n"
        return result

def update_task(jwt_token: str, task_id: int, title: str):
    """Update a task title. Requires a valid JWT token."""
    user_id = validate_token_and_get_user(jwt_token)
    
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task with ID {task_id} not found."
        
        task.title = title
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return f"Successfully updated task {task_id} to '{title}'."

def complete_task(jwt_token: str, task_id: int):
    """Mark a task as completed. Requires a valid JWT token."""
    user_id = validate_token_and_get_user(jwt_token)
    
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task with ID {task_id} not found."
        
        task.completed = True
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return f"Task {task_id} marked as completed."

def delete_task(jwt_token: str, task_id: int):
    """Delete a task. Requires a valid JWT token."""
    user_id = validate_token_and_get_user(jwt_token)
    
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task with ID {task_id} not found."
        
        session.delete(task)
        session.commit()
        return f"Successfully deleted task {task_id}."

# REGISTER MCP TOOLS

mcp.tool(name="add_task")(add_task)
mcp.tool(name="list_tasks")(list_tasks)
mcp.tool(name="update_task")(update_task)
mcp.tool(name="complete_task")(complete_task)
mcp.tool(name="delete_task")(delete_task)
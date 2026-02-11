import sys
import os
import uuid
import json

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.database.engine import engine, get_session
from src.models.user import User, UserCreate
from src.models.task import Task
from src.models.chat import Conversation, Message
from src.auth.jwt import create_access_token
from src.services.agent import run_todo_agent
from sqlmodel import Session, select

def setup_test_user():
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    with Session(engine) as session:
        user = User(
            email=email,
            hashed_password="hashed_password",
            first_name="Test",
            last_name="User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        token_data = {"sub": str(user.id), "email": user.email}
        token = create_access_token(data=token_data)
        return user, token

def test_flow():
    user, token = setup_test_user()
    print(f"Created test user: {user.email} (ID: {user.id})")
    print(f"Token: {token[:20]}...")

    history = []
    
    # 1. ADD TASK
    print("\n--- Operation 1: ADD TASK ---")
    message = "Add a task to buy groceries"
    response, conv_id, tool_calls = run_todo_agent(message, history, token)
    print(f"User: {message}")
    print(f"Agent: {response}")
    
    # Verify in DB
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == str(user.id))).all()
        print(f"Tasks in DB: {[t.title for t in tasks]}")
        assert any("groceries" in t.title.lower() for t in tasks)
        task_id = tasks[0].id

    # 2. LIST TASKS
    print("\n--- Operation 2: LIST TASKS ---")
    message = "Show me my tasks"
    history.append({"role": "USER", "message": "Add a task to buy groceries"})
    history.append({"role": "CHATBOT", "message": response})
    
    response, _, _ = run_todo_agent(message, history, token)
    print(f"User: {message}")
    print(f"Agent: {response}")
    assert str(task_id) in response or "groceries" in response.lower()

    # 3. COMPLETE TASK
    print("\n--- Operation 3: COMPLETE TASK ---")
    message = f"Mark task {task_id} as complete"
    response, _, _ = run_todo_agent(message, history, token)
    print(f"User: {message}")
    print(f"Agent: {response}")
    
    with Session(engine) as session:
        task = session.get(Task, task_id)
        print(f"Task {task_id} completed status: {task.completed}")
        assert task.completed == True

    # 4. DELETE TASK
    print("\n--- Operation 4: DELETE TASK ---")
    message = f"Delete task {task_id}"
    response, _, _ = run_todo_agent(message, history, token)
    print(f"User: {message}")
    print(f"Agent: {response}")
    
    with Session(engine) as session:
        task = session.get(Task, task_id)
        print(f"Task {task_id} exists: {task is not None}")
        assert task is None

    print("\n✅ ALL OPERATIONS COMPLETED SUCCESSFULLY (SCHEMA FIX VERIFIED)")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

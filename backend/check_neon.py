from src.database.engine import engine
from sqlmodel import Session, select
from src.models.user import User
from src.models.task import Task

def check_db():
    with Session(engine) as session:
        # Check Users
        users = session.exec(select(User)).all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"  - User: {u.email} (ID: {u.id})")
        
        # Check Tasks
        tasks = session.exec(select(Task)).all()
        print(f"Total Tasks: {len(tasks)}")
        for t in tasks:
            print(f"  - Task: {t.title} (User: {t.user_id}, Completed: {t.completed})")

if __name__ == "__main__":
    check_db()

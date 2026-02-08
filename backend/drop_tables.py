from src.database.engine import engine
from sqlmodel import SQLModel
# Import models to ensure they are registered with SQLModel.metadata
from src.models.user import User
from src.models.task import Task

def drop_all_tables():
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("All tables dropped successfully.")

if __name__ == "__main__":
    drop_all_tables()

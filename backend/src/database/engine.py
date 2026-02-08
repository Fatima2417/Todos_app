from sqlalchemy import create_engine
from sqlmodel import SQLModel
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with serverless PostgreSQL optimizations
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL query logging in development
)


def create_db_and_tables():
    """Create database tables based on SQLModel models"""
    SQLModel.metadata.create_all(engine)
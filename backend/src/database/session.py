from sqlmodel import Session
from .engine import engine


def get_session():
    """Generator function to yield database sessions"""
    with Session(engine) as session:
        yield session
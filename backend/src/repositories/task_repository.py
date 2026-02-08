from sqlmodel import Session, select, update, delete
from ..models.task import Task, TaskCreate, TaskUpdate
from typing import List, Optional
from datetime import datetime


def create_task_for_user(*, db: Session, user_id: str, task_data: TaskCreate) -> Task:
    """
    Create a new task for a specific user.

    Args:
        db: Database session
        user_id: The ID of the user creating the task
        task_data: Task creation data

    Returns:
        The created Task object
    """
    # Create task with user_id manually to avoid Pydantic validation error if user_id is missing in TaskCreate
    data = task_data.dict()
    task = Task(**data, user_id=user_id)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks_for_user(*, db: Session, user_id: str, completed_filter: Optional[bool] = None) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        db: Database session
        user_id: The ID of the user whose tasks to retrieve
        completed_filter: Optional filter for completed status (None for all, True for completed, False for incomplete)

    Returns:
        List of tasks belonging to the user
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed_filter is not None:
        query = query.where(Task.completed == completed_filter)

    return db.exec(query).all()


def get_task_by_id_for_user(*, db: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.

    Args:
        db: Database session
        task_id: The ID of the task to retrieve
        user_id: The ID of the user who owns the task

    Returns:
        The task if it exists and belongs to the user, None otherwise
    """
    query = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    return db.exec(query).first()


def update_task_for_user(*, db: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a specific task for a specific user.

    Args:
        db: Database session
        task_id: The ID of the task to update
        user_id: The ID of the user who owns the task
        task_update: Task update data

    Returns:
        The updated task if successful, None if task doesn't exist or doesn't belong to user
    """
    # Get the existing task to ensure it belongs to the user
    existing_task = get_task_by_id_for_user(db=db, task_id=task_id, user_id=user_id)
    if not existing_task:
        return None

    # Update the task with new data
    task_data = task_update.dict(exclude_unset=True)
    for field, value in task_data.items():
        setattr(existing_task, field, value)

    existing_task.updated_at = datetime.utcnow()

    db.add(existing_task)
    db.commit()
    db.refresh(existing_task)

    return existing_task


def delete_task_for_user(*, db: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a specific task for a specific user.

    Args:
        db: Database session
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task

    Returns:
        True if deletion was successful, False if task doesn't exist or doesn't belong to user
    """
    # Check if the task exists and belongs to the user
    existing_task = get_task_by_id_for_user(db=db, task_id=task_id, user_id=user_id)
    if not existing_task:
        return False

    # Delete the task
    db.delete(existing_task)
    db.commit()

    return True
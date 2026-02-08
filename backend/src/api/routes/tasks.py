from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session

from ...dependencies import get_db, validate_user_path
from ...schemas.task import TaskCreate, TaskUpdate, TaskPublic
from ...services.task_service import (
    create_task_for_user,
    get_tasks_for_user,
    get_task_by_id_for_user,
    update_task_for_user,
    delete_task_for_user,
    toggle_task_completion_for_user
)

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[TaskPublic])
def list_tasks(
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db),
    completed: Optional[bool] = None
):
    """
    List all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve (validated via JWT and path)
        db: Database session
        completed: Optional filter for completion status

    Returns:
        List of TaskPublic objects
    """
    try:
        tasks = get_tasks_for_user(db=db, user_id=user_id, completed_filter=completed)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db)
):
    """
    Create a new task for a specific user.

    Args:
        task_create: Task creation data
        user_id: The ID of the user creating the task (validated via JWT and path)
        db: Database session

    Returns:
        Created TaskPublic object
    """
    try:
        task = create_task_for_user(db=db, user_id=user_id, task_data=task_create)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(
    task_id: int,
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db)
):
    """
    Get a specific task for a specific user.

    Args:
        task_id: The ID of the task to retrieve
        user_id: The ID of the user requesting the task (validated via JWT and path)
        db: Database session

    Returns:
        TaskPublic object

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    try:
        task = get_task_by_id_for_user(db=db, task_id=task_id, user_id=user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@router.put("/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db)
):
    """
    Update a specific task for a specific user.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        user_id: The ID of the user updating the task (validated via JWT and path)
        db: Database session

    Returns:
        Updated TaskPublic object

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    try:
        updated_task = update_task_for_user(
            db=db,
            task_id=task_id,
            user_id=user_id,
            task_update=task_update
        )
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task for a specific user.

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user deleting the task (validated via JWT and path)
        db: Database session

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    try:
        success = delete_task_for_user(db=db, task_id=task_id, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion(
    task_id: int,
    user_id: str = Depends(validate_user_path),
    db: Session = Depends(get_db)
):
    """
    Toggle completion status of a specific task for a specific user.

    Args:
        task_id: The ID of the task to update
        user_id: The ID of the user updating the task (validated via JWT and path)
        db: Database session

    Returns:
        Updated TaskPublic object

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    try:
        updated_task = toggle_task_completion_for_user(
            db=db,
            task_id=task_id,
            user_id=user_id
        )
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task completion: {str(e)}"
        )
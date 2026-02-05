"""
Task data model for Todo In-Memory Python Console App
Manages in-memory storage and operations for tasks
"""

# Global variables for in-memory storage
tasks = []  # List to store all tasks
next_id = 1  # Counter for the next available task ID


def add_task(title, description=""):
    """
    Add a new task to the in-memory store

    Args:
        title (str): The task title (required)
        description (str): The task description (optional)

    Returns:
        dict: The created task with id, title, description, and completed status
    """
    global next_id

    # Validate input
    if not title or not isinstance(title, str) or len(title.strip()) == 0:
        raise ValueError("Task title is required and must be a non-empty string")

    # Create the new task
    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip() if description else "",
        "completed": False
    }

    # Add to the tasks list
    tasks.append(task)

    # Increment the ID counter
    next_id += 1

    return task


def get_all_tasks():
    """
    Retrieve all tasks from the in-memory store

    Returns:
        list: A list of all task dictionaries
    """
    return tasks


def get_task_by_id(task_id):
    """
    Retrieve a specific task by its ID

    Args:
        task_id (int): The unique identifier of the task

    Returns:
        dict: The task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(task_id, title=None, description=None):
    """
    Update an existing task's properties

    Args:
        task_id (int): The unique identifier of the task to update
        title (str, optional): New title if provided
        description (str, optional): New description if provided

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    if title is not None:
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Task title must be a non-empty string if provided")
        task["title"] = title.strip()

    if description is not None:
        task["description"] = description.strip() if description else ""

    return True


def delete_task(task_id):
    """
    Remove a task from the in-memory store by ID

    Args:
        task_id (int): The unique identifier of the task to delete

    Returns:
        bool: True if successful, False if task not found
    """
    global tasks
    initial_length = len(tasks)

    # Filter out the task with the given ID
    tasks = [task for task in tasks if task["id"] != task_id]

    # Check if any task was removed
    return len(tasks) != initial_length


def toggle_task_completion(task_id):
    """
    Toggle the completion status of a task

    Args:
        task_id (int): The unique identifier of the task to update

    Returns:
        bool: True if successful, False if task not found
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    task["completed"] = not task["completed"]
    return True


def reset_storage():
    """
    Reset the in-memory storage for testing purposes
    """
    global tasks, next_id
    tasks = []
    next_id = 1
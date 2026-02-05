# CLI API Contract: Todo In-Memory Python Console App

## Overview
This document describes the CLI interface contracts for the Todo application.

## Function Signatures

### add_task(title: str, description: str = "") -> dict
**Purpose**: Adds a new task to the in-memory store
**Parameters**:
- `title` (str): Required task title (1-200 characters)
- `description` (str): Optional task description (up to 1000 characters)
**Returns**: Task dictionary with id, title, description, and completed status
**Example**:
```python
task = add_task("Buy groceries", "Milk, bread, eggs")
# Returns: {"id": 1, "title": "Buy groceries", "description": "Milk, bread, eggs", "completed": False}
```

### delete_task(task_id: int) -> bool
**Purpose**: Removes a task from the store by ID
**Parameters**:
- `task_id` (int): The unique identifier of the task to delete
**Returns**: True if successful, False if task not found
**Example**:
```python
success = delete_task(1)  # Returns True if successful
```

### update_task(task_id: int, title: str = None, description: str = None) -> bool
**Purpose**: Updates an existing task's properties
**Parameters**:
- `task_id` (int): The unique identifier of the task to update
- `title` (str, optional): New title if provided
- `description` (str, optional): New description if provided
**Returns**: True if successful, False if task not found
**Example**:
```python
success = update_task(1, title="Updated title", description="Updated description")
```

### get_all_tasks() -> list
**Purpose**: Retrieves all tasks from the store
**Returns**: List of all task dictionaries
**Example**:
```python
tasks = get_all_tasks()
# Returns: [{"id": 1, "title": "...", ...}, ...]
```

### toggle_task_completion(task_id: int) -> bool
**Purpose**: Toggles the completion status of a task
**Parameters**:
- `task_id` (int): The unique identifier of the task to update
**Returns**: True if successful, False if task not found
**Example**:
```python
success = toggle_task_completion(1)  # Toggles completed status
```

## Data Models

### Task Object
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "completed": true
}
```

## Error Handling
- Invalid task ID: Function returns False
- Empty title: Appropriate error message to user
- Non-existent operation: Appropriate error message to user
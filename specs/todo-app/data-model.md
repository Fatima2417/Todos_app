# Data Model: Todo In-Memory Python Console App

## Task Entity

### Fields
- **id** (int): Unique identifier for the task (auto-incremented)
- **title** (str): Task title/description (required)
- **description** (str): Optional detailed description of the task
- **completed** (bool): Boolean indicating task completion status (default: False)

### Structure
```python
{
    "id": int,
    "title": str,
    "description": str,
    "completed": bool
}
```

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string (1-200 characters)
- `description` can be empty or string up to 1000 characters
- `completed` must be boolean (True/False)

## Task Collection

### Structure
- **tasks** (list): A list containing all task dictionaries
- **next_id** (int): Counter for the next available task ID (starts at 1, increments by 1)

### Example
```python
tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, bread, eggs, fruits",
        "completed": False
    },
    {
        "id": 2,
        "title": "Finish project",
        "description": "Complete the todo app implementation",
        "completed": True
    }
]
next_id = 3
```

## State Transitions

### Task Completion States
- **Incomplete** (False): Default state when task is created
- **Complete** (True): State when task is marked as completed
- **Toggle**: Transition possible from either state to the other

## Operations

### Create Task
- Generate new ID using `next_id`
- Increment `next_id` counter
- Set `completed` to False by default
- Require `title` parameter
- Allow optional `description` parameter

### Read Tasks
- Return entire task list for viewing
- Filter by completion status if needed

### Update Task
- Modify existing task attributes
- Preserve original ID
- Allow partial updates (title or description separately)

### Delete Task
- Remove task from collection
- Do not affect other tasks' IDs
- Preserve order where possible

### Mark Complete/Incomplete
- Flip the boolean value of `completed` field
- Accept task ID as parameter
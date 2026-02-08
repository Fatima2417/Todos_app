# Quickstart Guide: Database Layer Setup

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Neon PostgreSQL account with a serverless project created
- Environment variables configured (see Configuration section)

## Installation

1. Install the project dependencies:

```bash
pip install sqlmodel sqlalchemy psycopg2-binary python-dotenv
```

Or using Poetry:

```bash
poetry add sqlmodel sqlalchemy psycopg2-binary python-dotenv
```

2. Set up environment variables (copy `.env.example` to `.env` and fill in values)

## Configuration

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

## Database Initialization

To initialize the database tables:

```python
from backend.src.database.engine import engine
from backend.src.models import User, Task

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

## Usage Examples

### Creating a Task

```python
from backend.src.repositories.task_repository import create_task
from backend.src.models.task import TaskCreate

task_data = TaskCreate(title="Sample Task", description="Sample Description")
new_task = create_task(task_data, user_id="user123")
```

### Reading Tasks for a User

```python
from backend.src.repositories.task_repository import get_tasks_by_user

user_tasks = get_tasks_by_user(user_id="user123")
```

### Updating a Task

```python
from backend.src.repositories.task_repository import update_task
from backend.src.models.task import TaskUpdate

update_data = TaskUpdate(title="Updated Task", completed=True)
updated_task = update_task(task_id=1, task_update=update_data, user_id="user123")
```

### Deleting a Task

```python
from backend.src.repositories.task_repository import delete_task

delete_task(task_id=1, user_id="user123")
```

## Security Note

All database operations enforce user isolation by requiring the `user_id` parameter and filtering queries based on this value to prevent unauthorized access to other users' data.
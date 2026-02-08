---
name: database-skill
description: Design schemas, create tables, and manage migrations for Neon Serverless PostgreSQL using SQLModel. Provides patterns for secure, user-isolated data structures.
---

# Database Schema & Migration Skill

## Core Responsibilities

1.  **Schema Design & Modeling**
    *   Define SQLModel classes that map directly to database tables.
    *   Establish correct relationships (foreign keys) between tables (e.g., `Task.user_id` → `User.id`).
    *   Choose appropriate data types (e.g., `String`, `Integer`, `DateTime`, `Boolean`).
    *   Define constraints like `nullable=False`, `unique=True`, and `index=True` for performance.

2.  **Table Creation & Management**
    *   Generate initial tables from SQLModel definitions programmatically.
    *   Use `SQLModel.metadata.create_all()` for initial setup in development.
    *   Plan and execute schema changes (adding/removing columns, changing types).

3.  **Migration Management**
    *   Use **Alembic** (SQLModel's underlying migration tool) to create and apply incremental migration scripts.
    *   Write both `upgrade()` (apply changes) and `downgrade()` (revert changes) functions in migration files.
    *   Maintain a linear, version-controlled migration history.

4.  **Connection & Session Handling**
    *   Configure the database engine using the `DATABASE_URL` from Neon.
    *   Properly manage database sessions: open, commit, rollback, and close.
    *   Implement connection pooling suitable for a serverless environment.

## Instructions

### 1. Defining SQLModel Schemas

Create your data models in a file like `src/models.py`. Each class should inherit from `SQLModel` and include a `Table` configuration.

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# User model (likely managed by Better Auth, but referenced by tasks)
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(primary_key=True) # Matches Better Auth user ID
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Core Task model for the Todo app
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    # CRITICAL: Foreign key for user data isolation
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. Initial Schema Creation

For the first setup, you can create all tables directly from the models. This is suitable for early development.

```python
# src/database.py
from sqlmodel import SQLModel, create_engine
import os
from . import models # Import your models to register them

# Get connection string from environment (configure in Neon dashboard)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Create all tables based on SQLModel metadata. Use for initial setup."""
    SQLModel.metadata.create_all(engine)
```

### 3. Managing Migrations with Alembic

For production and collaborative development, use Alembic to manage incremental changes.

A. Initialize Alembic (Run once):

```bash
alembic init alembic
```

B. Configure alembic.ini and env.py:
Ensure env.py uses your SQLModel setup and imports your model's Base.metadata.

C. Create a Migration (After changing a model):

```bash
# Autogenerate a migration script by comparing models to current DB state
alembic revision --autogenerate -m "Add due_date field to tasks"
```

D. Review and Apply the Migration:
Check the generated script in alembic/versions/, then apply it:

```bash
alembic upgrade head
```

## Best Practices

### Security & Data Integrity
- Always Filter by user_id: Every query for user data (like tasks) must include a WHERE user_id = :current_user_id clause. This is the primary security rule.
- Use Foreign Keys: Enforce relational integrity at the database level. This prevents orphaned records.
- Parameterize Queries: Never use string formatting (f"...") to insert values into SQL. Always use SQLModel's ORM or parameterized queries to prevent SQL injection.

### Schema Design
- Keep IDs Simple: Use an auto-incrementing integer (Integer, primary_key=True) for internal task IDs. Use the external auth provider's ID (a string) for the user_id foreign key.
- Add Indexes Strategically: Add database indexes on columns frequently used in WHERE, ORDER BY, or JOIN clauses (e.g., user_id, completed). This is crucial for performance with many tasks.
- Use Sensible Defaults: Use default_factory for timestamps (datetime.utcnow) and booleans (False).

### Migration Strategy
- Test Migrations Locally First: Always run alembic upgrade head and alembic downgrade -1 on a local/test database before applying to production.
- Keep Migrations Small: Each migration should ideally do one thing (add a column, create an index). This makes them easier to debug and roll back.
- Version Control Migrations: Commit all Alembic migration scripts (alembic/versions/) to your Git repository.

### Example Migration File

A typical autogenerated Alembic migration script looks like this:

```python
# alembic/versions/2025_02_06_1337_add_due_date_field.py
"""Add due_date field to tasks

Revision ID: a1b2c3d4e5f6
Revises: previous_revision_id
Create Date: 2025-02-06 13:37:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add the new column
    op.add_column('tasks',
        sa.Column('due_date', sa.DateTime(), nullable=True)
    )

def downgrade() -> None:
    # Remove the column if rolling back
    op.drop_column('tasks', 'due_date')
```

## Troubleshooting Common Issues
- "Relation does not exist": The table hasn't been created. Run create_db_and_tables() or apply pending migrations with alembic upgrade head.
- Autogenerate doesn't detect changes: Ensure your model classes are imported in your Alembic env.py file so they are part of the model metadata Alembic scans.
- Connection errors to Neon: Verify your DATABASE_URL is correct and that your IP is allowed in Neon's dashboard if using IP-based restrictions. For serverless functions, use Neon's connection pooling.
- Foreign key violation: You are trying to insert a task with a user_id that does not exist in the users table. Ensure the user is created (via Better Auth) before creating their tasks.
# Data Model: Database Schema & Serverless Operations

## Entities

### User
Represents an authenticated user in the system

**Fields**:
- `id`: string (primary key) - Unique identifier from Better Auth
- `email`: string (unique, indexed) - User's email address
- `created_at`: datetime - Timestamp of account creation

**Validation rules**:
- `id` must be non-empty string (from Better Auth)
- `email` must be valid email format
- `email` must be unique across all users

**Relationships**:
- One-to-many with Task (via `user_id` foreign key)

### Task
Represents a todo item created by a user

**Fields**:
- `id`: integer (auto-increment, primary key) - Unique task identifier
- `title`: string (max 200 characters, not null) - Task title
- `description`: string (optional, max 1000 characters) - Detailed task description
- `completed`: boolean - Completion status (default: False)
- `user_id`: string (foreign key, indexed, not null) - Link to owning user
- `created_at`: datetime - Timestamp of task creation
- `updated_at`: datetime - Timestamp of last update

**Validation rules**:
- `title` must be non-empty and ≤ 200 characters
- `description` can be null or ≤ 1000 characters
- `completed` defaults to False
- `user_id` must correspond to an existing User
- `user_id` is indexed for query performance

**State transitions**:
- `completed`: False → True (mark as complete)
- `completed`: True → False (mark as incomplete)
- `title`/`description`: editable anytime

**Relationships**:
- Many-to-one with User (via `user_id` foreign key)
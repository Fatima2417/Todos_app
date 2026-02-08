# Data Model: RESTful API & Business Logic

## API Schemas

### TaskCreate (Request Schema)
Schema for validating new task creation requests

**Fields**:
- `title`: string (required, min_length=1, max_length=200) - The task title
- `description`: string (optional, max_length=1000) - Detailed task description

**Validation rules**:
- `title` must be non-empty and ≤ 200 characters
- `description` can be null or ≤ 1000 characters
- All fields undergo automatic validation via Pydantic

### TaskUpdate (Request Schema)
Schema for validating task update requests

**Fields**:
- `title`: string (optional, min_length=1, max_length=200) - Updated task title
- `description`: string (optional, max_length=1000) - Updated task description
- `completed`: boolean (optional) - Updated completion status

**Validation rules**:
- If `title` is provided, it must be ≤ 200 characters
- If `description` is provided, it must be ≤ 1000 characters
- Fields not provided will be ignored (partial updates)

### TaskPublic (Response Schema)
Schema for serializing task responses for external consumption

**Fields**:
- `id`: integer - Unique task identifier
- `title`: string - The task title
- `description`: string (optional) - Task description
- `completed`: boolean - Completion status
- `created_at`: datetime - Timestamp of task creation
- `updated_at`: datetime - Timestamp of last update

**Serialization rules**:
- Converts ORM objects to JSON using `from_attributes=True`
- Excludes sensitive fields not meant for client consumption
- Provides consistent response format across all endpoints

## API Endpoints

### GET /api/v1/{user_id}/tasks
**Operation**: List all tasks for a specific user
**Authentication**: JWT token required
**Parameters**: user_id (path), completed_filter (query, optional)
**Response**: Array of TaskPublic objects

### POST /api/v1/{user_id}/tasks
**Operation**: Create a new task for a specific user
**Authentication**: JWT token required
**Parameters**: user_id (path), TaskCreate (request body)
**Response**: Created TaskPublic object

### GET /api/v1/{user_id}/tasks/{task_id}
**Operation**: Get a specific task for a specific user
**Authentication**: JWT token required
**Parameters**: user_id (path), task_id (path)
**Response**: TaskPublic object

### PUT /api/v1/{user_id}/tasks/{task_id}
**Operation**: Update a specific task for a specific user
**Authentication**: JWT token required
**Parameters**: user_id (path), task_id (path), TaskUpdate (request body)
**Response**: Updated TaskPublic object

### DELETE /api/v1/{user_id}/tasks/{task_id}
**Operation**: Delete a specific task for a specific user
**Authentication**: JWT token required
**Parameters**: user_id (path), task_id (path)
**Response**: Empty (204 No Content)

### PATCH /api/v1/{user_id}/tasks/{task_id}/complete
**Operation**: Toggle completion status of a specific task
**Authentication**: JWT token required
**Parameters**: user_id (path), task_id (path), completed (request body)
**Response**: Updated TaskPublic object

## Dependencies & Validation

### JWT Token Validation
**Function**: `get_current_user` (from P2-SPEC-1)
**Purpose**: Extract and validate user identity from JWT token
**Flow**: Token → Decode → Verify Signature → Extract User ID

### Path Parameter Validation
**Function**: `validate_user_path` (custom dependency)
**Purpose**: Ensure JWT user_id matches path user_id parameter
**Flow**: JWT user_id ↔ Path user_id → Match/Reject
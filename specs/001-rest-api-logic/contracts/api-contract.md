# API Contract: Todo REST API

## Base URL
`https://api.yourdomain.com/api/v1`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Responses
```json
{
  "data": { /* response object */ },
  "message": "Success message"
}
```

### Error Responses
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional details */ }
  }
}
```

## Endpoints

### List Tasks
**GET** `/users/{user_id}/tasks`

#### Parameters
- `user_id` (path): User ID (must match JWT token)
- `completed` (query, optional): Filter by completion status

#### Headers
- `Authorization: Bearer <token>`

#### Response
- `200`: List of Task objects
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `422`: Validation error

### Create Task
**POST** `/users/{user_id}/tasks`

#### Parameters
- `user_id` (path): User ID (must match JWT token)

#### Headers
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

#### Body
```json
{
  "title": "Task title",
  "description": "Task description"
}
```

#### Response
- `201`: Created Task object
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `422`: Validation error

### Get Task
**GET** `/users/{user_id}/tasks/{task_id}`

#### Parameters
- `user_id` (path): User ID (must match JWT token)
- `task_id` (path): Task ID

#### Headers
- `Authorization: Bearer <token>`

#### Response
- `200`: Task object
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `404`: Task not found
- `422`: Validation error

### Update Task
**PUT** `/users/{user_id}/tasks/{task_id}`

#### Parameters
- `user_id` (path): User ID (must match JWT token)
- `task_id` (path): Task ID

#### Headers
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

#### Body
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": false
}
```

#### Response
- `200`: Updated Task object
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `404`: Task not found
- `422`: Validation error

### Delete Task
**DELETE** `/users/{user_id}/tasks/{task_id}`

#### Parameters
- `user_id` (path): User ID (must match JWT token)
- `task_id` (path): Task ID

#### Headers
- `Authorization: Bearer <token>`

#### Response
- `204`: No content (success)
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `404`: Task not found
- `422`: Validation error

### Update Task Completion
**PATCH** `/users/{user_id}/tasks/{task_id}/complete`

#### Parameters
- `user_id` (path): User ID (must match JWT token)
- `task_id` (path): Task ID

#### Headers
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

#### Body
```json
{
  "completed": true
}
```

#### Response
- `200`: Updated Task object
- `401`: Unauthorized
- `403`: Forbidden (user_id mismatch)
- `404`: Task not found
- `422`: Validation error

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid JWT token |
| `FORBIDDEN` | 403 | User ID in token doesn't match path parameter |
| `NOT_FOUND` | 404 | Requested resource doesn't exist |
| `VALIDATION_ERROR` | 422 | Request body fails validation |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Pydantic Schemas

### Task Schema
```python
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### TaskCreate Schema
```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

### TaskUpdate Schema
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
```
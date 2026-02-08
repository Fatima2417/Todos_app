# Todo App API Layer

This directory contains the backend API implementation for the Todo application, with a focus on the secure, validated REST API.

## API Architecture

### Endpoints
All endpoints follow the pattern: `/{version}/{user_id}/tasks`

1. **GET** `/api/v1/{user_id}/tasks` - List all tasks for user
2. **POST** `/api/v1/{user_id}/tasks` - Create new task
3. **GET** `/api/v1/{user_id}/tasks/{task_id}` - Get specific task
4. **PUT** `/api/v1/{user_id}/tasks/{task_id}` - Update full task
5. **DELETE** `/api/v1/{user_id}/tasks/{task_id}` - Delete task
6. **PATCH** `/api/v1/{user_id}/tasks/{task_id}/complete` - Toggle completion

### Security Implementation
- **JWT Authentication**: All endpoints require a valid JWT token in the Authorization header
- **Path Validation**: The `{user_id}` in the path must match the user ID in the JWT token
- **User Isolation**: Users can only access their own tasks

### Request/Response Schemas
- **TaskCreate**: `{title: string, description?: string}`
- **TaskUpdate**: `{title?: string, description?: string, completed?: boolean}`
- **TaskPublic**: `{id: number, title: string, description?: string, completed: boolean, created_at: date, updated_at: date}`

### Error Handling
- Returns structured JSON error responses
- Appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 422, 500)

### Dependencies
- FastAPI framework with automatic documentation
- Pydantic models for validation
- Integration with the task repository layer from the database implementation

## Usage
- Access the interactive API documentation at `/docs`
- All endpoints require proper JWT token authentication
- The user_id in the path must match the user_id in the JWT token
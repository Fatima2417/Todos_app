# Quickstart Guide: API Layer Setup

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Backend service with JWT authentication (P2-SPEC-1) running
- Database service with task repository (P2-SPEC-2) running
- Environment variables configured (see Configuration section)

## Installation

1. Install the project dependencies:

```bash
pip install fastapi uvicorn python-multipart pydantic
```

Or using Poetry:

```bash
poetry add fastapi uvicorn python-multipart pydantic
```

2. Set up environment variables (copy `.env.example` to `.env` and fill in values)

## Configuration

Create a `.env` file with the necessary variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the API

1. Start the development server:

```bash
uvicorn app:app --reload
```

2. Visit `http://localhost:8000/docs` to access the interactive API documentation

## API Usage Examples

### Creating a Task

```bash
curl -X POST "http://localhost:8000/api/v1/user123/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "Sample Description"}'
```

### Listing Tasks for a User

```bash
curl -X GET "http://localhost:8000/api/v1/user123/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Updating a Task

```bash
curl -X PUT "http://localhost:8000/api/v1/user123/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "completed": true}'
```

### Deleting a Task

```bash
curl -X DELETE "http://localhost:8000/api/v1/user123/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Security Note

The API enforces the critical security rule that the `user_id` extracted from the JWT token must match the `user_id` in the request path. This prevents users from accessing or manipulating other users' tasks.
# API Contract: Task Database Operations

## Overview

These are the database-level operations that will be exposed to the service layer. These operations enforce user data isolation by requiring a `user_id` parameter and automatically filtering results by that user.

## Operations

### CREATE Task

**Method**: `POST /tasks`

**Input**:
```json
{
  "title": "string (required, max 200)",
  "description": "string (optional, max 1000)",
  "user_id": "string (required)"
}
```

**Output**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Database Operation**: INSERT INTO tasks (title, description, completed, user_id, created_at, updated_at) VALUES (?, ?, FALSE, ?, NOW(), NOW())

**Security**: Links the task to the specified user_id

---

### READ Tasks by User

**Method**: `GET /tasks?user_id={user_id}`

**Input**:
- `user_id`: string (required)

**Output**:
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "user_id": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

**Database Operation**: SELECT * FROM tasks WHERE user_id = ?

**Security**: Only returns tasks belonging to the specified user

---

### READ Single Task

**Method**: `GET /tasks/{task_id}?user_id={user_id}`

**Input**:
- `task_id`: integer (required, path parameter)
- `user_id`: string (required, query parameter)

**Output**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Database Operation**: SELECT * FROM tasks WHERE id = ? AND user_id = ?

**Security**: Only returns task if it belongs to the specified user

---

### UPDATE Task

**Method**: `PUT /tasks/{task_id}`

**Input**:
```json
{
  "task_id": "integer (required, path)",
  "user_id": "string (required, body/query)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Output**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Database Operation**: UPDATE tasks SET title = COALESCE(?, title), description = COALESCE(?, description), completed = COALESCE(?, completed), updated_at = NOW() WHERE id = ? AND user_id = ?

**Security**: Only updates task if it belongs to the specified user

---

### DELETE Task

**Method**: `DELETE /tasks/{task_id}?user_id={user_id}`

**Input**:
- `task_id`: integer (required, path parameter)
- `user_id`: string (required, query parameter)

**Output**: Empty body, HTTP 204

**Database Operation**: DELETE FROM tasks WHERE id = ? AND user_id = ?

**Security**: Only deletes task if it belongs to the specified user

---

### TOGGLE Task Completion

**Method**: `PATCH /tasks/{task_id}/complete`

**Input**:
- `task_id`: integer (required, path parameter)
- `user_id`: string (required, body/query)
- `completed`: boolean (required)

**Output**:
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Database Operation**: UPDATE tasks SET completed = ?, updated_at = NOW() WHERE id = ? AND user_id = ?

**Security**: Only updates task if it belongs to the specified user
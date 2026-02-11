# API Contracts: AI-Powered Todo Chatbot

## Chat Endpoint

**POST** `/api/chat`

- **Description**: Secure endpoint to send a user message and receive an AI response.
- **Authentication**: Bearer JWT required.
- **Request Body**:
  ```json
  {
    "message": "Add a task to buy groceries"
  }
  ```
- **Response Body**:
  ```json
  {
    "response": "I've added 'buy groceries' to your task list.",
    "conversation_id": "uuid-v4-string"
  }
  ```

## MCP Tools (Task Management)

The following tools are exposed by the MCP Server:

### `add_task`
- **Arguments**: `title` (string)
- **Description**: Creates a new task for the authenticated user.

### `list_tasks`
- **Arguments**: None
- **Description**: Returns all pending tasks for the authenticated user.

### `update_task`
- **Arguments**: `task_id` (int), `title` (string)
- **Description**: Updates the title of an existing task.

### `complete_task`
- **Arguments**: `task_id` (int)
- **Description**: Marks a task as completed.

### `delete_task`
- **Arguments**: `task_id` (int)
- **Description**: Deletes a task.

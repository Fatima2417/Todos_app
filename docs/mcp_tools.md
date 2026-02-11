# MCP Tool Specifications: Todo Assistant

The Todo Assistant MCP server exposes the following standardized tools for managing tasks via natural language.

## Authentication
All tools require a valid `jwt_token` passed as a string. The server extracts the `user_id` from the token to ensure data isolation.

## Tool Definitions

### `add_task`
- **Description**: Creates a new task for the user.
- **Parameters**:
  - `jwt_token` (string, required): Valid user JWT.
  - `title` (string, required): The task title.
  - `description` (string, optional): Detailed task description.
- **Returns**: Confirmation string with the new task ID.

### `list_tasks`
- **Description**: Returns all pending (incomplete) tasks for the user.
- **Parameters**:
  - `jwt_token` (string, required): Valid user JWT.
- **Returns**: A formatted list of pending tasks or a "no tasks" message.

### `update_task`
- **Description**: Updates the title of an existing task.
- **Parameters**:
  - `jwt_token` (string, required): Valid user JWT.
  - `task_id` (integer, required): The ID of the task to update.
  - `title` (string, required): The new title.
- **Returns**: Confirmation string.

### `complete_task`
- **Description**: Marks a specific task as completed.
- **Parameters**:
  - `jwt_token` (string, required): Valid user JWT.
  - `task_id` (integer, required): The ID of the task to complete.
- **Returns**: Confirmation string.

### `delete_task`
- **Description**: Permanently removes a task.
- **Parameters**:
  - `jwt_token` (string, required): Valid user JWT.
  - `task_id` (integer, required): The ID of the task to delete.
- **Returns**: Confirmation string.

## Security
User isolation is strictly enforced at the tool level. If a user provides a `task_id` that does not belong to them, the tool will return a "not found" error.

# API Contracts: Frontend-Backend Integration

## Authentication API Contracts (from P2-SPEC-1)

### Better Auth Integration
- **Token Management**: Better Auth provides JWT tokens that must be included in Authorization header
- **Auth State**: React Context must provide isLoggedIn, user, and auth functions
- **Redirects**: Unauthenticated users redirected to login page

## Backend API Contracts (from P2-SPEC-3)

### Task Management Endpoints

#### GET /api/v1/{user_id}/tasks
**Request**:
- Headers: `Authorization: Bearer {token}`
- Params: `user_id` (from JWT, validated to match path)
- Query: `completed` (optional filter)

**Response**:
- 200: `Task[]` - Array of user's tasks
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)
- 404: Not found

#### POST /api/v1/{user_id}/tasks
**Request**:
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Params: `user_id` (from JWT, validated to match path)
- Body: `TaskCreate` object

**Response**:
- 201: `Task` - Created task object
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)

#### GET /api/v1/{user_id}/tasks/{task_id}
**Request**:
- Headers: `Authorization: Bearer {token}`
- Params: `user_id` (from JWT), `task_id`

**Response**:
- 200: `Task` - Specific task object
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)
- 404: Task not found

#### PUT /api/v1/{user_id}/tasks/{task_id}
**Request**:
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Params: `user_id` (from JWT), `task_id`
- Body: `TaskUpdate` object

**Response**:
- 200: `Task` - Updated task object
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)
- 404: Task not found

#### DELETE /api/v1/{user_id}/tasks/{task_id}
**Request**:
- Headers: `Authorization: Bearer {token}`
- Params: `user_id` (from JWT), `task_id`

**Response**:
- 204: No content (success)
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)
- 404: Task not found

#### PATCH /api/v1/{user_id}/tasks/{task_id}/complete
**Request**:
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Params: `user_id` (from JWT), `task_id`
- Body: `{ completed: boolean }`

**Response**:
- 200: `Task` - Updated task object
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden (user_id mismatch)
- 404: Task not found

## Error Response Format
All error responses follow the format:
````
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Descriptive error message",
    "details": {} // optional
  }
}
````

## Frontend-Backend Interface Specifications

### Loading States
- **Data Fetching**: Show skeleton loaders while API calls are in progress
- **Form Submission**: Disable form and show submitting indicator
- **Page Transitions**: Show loading spinner during navigation

### Error Handling
- **Network Errors**: Show user-friendly messages and retry options
- **Validation Errors**: Highlight problematic fields and display error messages
- **Unauthorized Access**: Redirect to login page automatically

### Data Consistency
- **Optimistic Updates**: Update UI immediately for better UX, rollback on error
- **Cache Invalidation**: Invalidate relevant queries after mutations
- **Polling/Fetching Strategies**: Implement appropriate refetching for data consistency
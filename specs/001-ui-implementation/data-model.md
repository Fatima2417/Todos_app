# Data Model: Responsive Web Interface for Todo Web App

## UI Components

### Layout Components
- **Header**: Navigation bar with auth state awareness and user menu
- **Container**: Responsive grid container for consistent page structure
- **Sidebar**: (Optional) Navigation sidebar for dashboard pages

### Task Components
- **TaskCard**: Display individual task with title, description, completion status, and action buttons
- **TaskList**: Container for multiple TaskCard components with loading states
- **TaskForm**: Form for creating and editing tasks with validation

### UI Elements
- **Button**: Reusable button component with different variants (primary, secondary, danger)
- **Input**: Reusable input field with validation states
- **Modal**: Overlay component for confirmation dialogs
- **Alert**: Component for displaying error/success messages

### Authentication Components
- **LoginForm**: Form for user authentication
- **SignupForm**: Form for user registration
- **AuthWrapper**: Component that renders different UI based on auth state

## Client-Side State Model

### User State (Managed via React Context)
- **isLoggedIn**: Boolean indicating authentication status
- **user**: Object containing user details (id, email, etc.)
- **isLoading**: Boolean for authentication loading states

### Task State (Managed via TanStack Query)
- **tasks**: Array of task objects from API
- **isLoading**: Boolean for task data loading states
- **error**: Error object for failed requests
- **filters**: Current filters applied to the task list (completed/incomplete)

### Task Object Structure (Matches API response)
```
{
  id: number,
  title: string,
  description: string | null,
  completed: boolean,
  created_at: Date,
  updated_at: Date
}
```

### Form State (Managed via React Hook Form)
- **formData**: Current values in form fields
- **errors**: Validation errors for each field
- **isSubmitting**: Boolean indicating form submission status

## API Integration Patterns

### Authentication Endpoints (via Better Auth)
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - User session termination

### Task Management Endpoints (via FastAPI)
- `GET /api/v1/{user_id}/tasks` - List all user tasks
- `POST /api/v1/{user_id}/tasks` - Create new task
- `GET /api/v1/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/v1/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/v1/{user_id}/tasks/{task_id}/complete` - Toggle completion status

## Types Definitions (TypeScript)

### User Interface
````
interface User {
  id: string;
  email: string;
  createdAt: Date;
}
````

### Task Interface
````
interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: Date;
  updated_at: Date;
}
````

### Form Data Interfaces
````
interface TaskFormData {
  title: string;
  description?: string;
  completed?: boolean;
}

interface LoginFormInputs {
  email: string;
  password: string;
}

interface SignupFormInputs {
  email: string;
  password: string;
  confirmPassword: string;
}
````

## Responsive Breakpoints

### Screen Sizes
- **Mobile**: Up to 640px (Tailwind sm)
- **Tablet**: 641px to 1024px (Tailwind md/lg)
- **Desktop**: Above 1024px (Tailwind xl+)

### Layout Adjustments
- **Mobile**: Single column layout, simplified navigation
- **Tablet**: Two column layouts where appropriate
- **Desktop**: Multi-column layouts with full feature set
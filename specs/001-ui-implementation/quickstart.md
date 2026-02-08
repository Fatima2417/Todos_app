# Quickstart Guide: Frontend Development Environment

## Prerequisites

- Node.js 18+ installed
- pnpm package manager installed (recommended) or npm/yarn
- Git for version control
- A modern web browser for development and testing

## Setup Instructions

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pnpm install
# or npm install or yarn install
```

3. Create environment variables file `.env.local` with the required configuration:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

4. Start the development server:
```bash
pnpm dev
# or npm run dev or yarn dev
```

5. Visit `http://localhost:3000` in your browser to see the application

## Development Workflow

### Adding a New Component
1. Create the component file in `frontend/components/`
2. Add proper TypeScript interfaces and Tailwind CSS classes
3. Write unit tests for the component
4. Export the component in the appropriate index file

### Adding a New Page
1. Create the page file in `frontend/app/` following the App Router structure
2. Implement proper loading and error boundaries
3. Add any necessary API integration code

### Connecting to Backend APIs
1. Update the API client in `frontend/lib/api-client.ts`
2. Create or update react-query hooks for data management
3. Handle loading/error states appropriately in UI components

### Styling Components
1. Use Tailwind CSS utility classes directly in components
2. Follow the established design system and color palette
3. Ensure responsive design across all breakpoints

## Available Scripts

- `pnpm dev` - Start development server with hot reloading
- `pnpm build` - Build the application for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint for code quality checks
- `pnpm test` - Run unit tests
- `pnpm test:e2e` - Run end-to-end tests

## Common Integration Patterns

### Authentication Flow
```typescript
import { useAuth } from '@/hooks/useAuth';

export default function ProtectedPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Please log in</div>;

  return <div>Protected content</div>;
}
```

### API Data Fetching
```typescript
import { useTasks } from '@/lib/tasks-query';

export default function TaskList() {
  const { data: tasks, isLoading } = useTasks();

  if (isLoading) return <SkeletonLoader />;

  return (
    <div>
      {tasks?.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}
```

### Form Handling
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { taskSchema } from '@/lib/validation';

export default function TaskForm() {
  const form = useForm({
    resolver: zodResolver(taskSchema)
  });

  // Use form methods in your component
}
```
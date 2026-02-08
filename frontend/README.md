# Todo App Frontend

This directory contains the Next.js frontend for the Todo application with secure, user-isolated task management.

## Features

- **Secure Authentication**: Integration with Better Auth for JWT-based authentication
- **Task Management**: Full CRUD operations for user-specific tasks
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Type Safety**: Full TypeScript coverage with interface definitions
- **State Management**: React Context for authentication state and TanStack Query for server state

## Architecture

### Directory Structure
```
frontend/
├── app/                    # Next.js 16+ App Router pages
│   ├── layout.tsx          # Root layout with AuthProvider
│   ├── page.tsx            # Home/landing page
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── signup/
│   │   └── page.tsx        # Signup page
│   └── dashboard/
│       ├── layout.tsx      # Dashboard layout
│       └── page.tsx        # Main dashboard page
├── components/             # Reusable React components
│   ├── auth/               # Authentication components
│   ├── layout/             # Layout components
│   ├── tasks/              # Task management components
│   └── ui/                 # Base UI components
├── lib/                    # Shared utilities and API clients
│   ├── api-client.ts       # API client with JWT integration
│   ├── auth-context.tsx    # Authentication context provider
│   ├── tasks-query.ts      # TanStack Query hooks for task operations
│   └── types.ts            # TypeScript interfaces
├── hooks/                  # Custom React hooks
│   └── useAuth.ts          # Authentication state hook
└── styles/                 # Global styles
```

### Security Implementation
- JWT tokens from Better Auth automatically attached to all API requests
- User ID validation ensures requests match authenticated user
- All task operations filtered by user ID at the backend level

### API Integration
The frontend communicates with the backend through six secured REST endpoints:
- `GET /api/{user_id}/tasks` - Retrieve user's tasks
- `POST /api/{user_id}/tasks` - Create new task for user
- `GET /api/{user_id}/tasks/{id}` - Retrieve specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Environment Variables

Create a `.env.local` file in this directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Development

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Dependencies

- Next.js 16+ with App Router
- React 18+ with TypeScript
- Tailwind CSS for styling
- TanStack Query (React Query) for server state management
- React Hook Form for form handling
- Better Auth for authentication
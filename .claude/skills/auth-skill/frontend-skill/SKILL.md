---
name: frontend-skill
description: Build responsive, interactive user interfaces with Next.js 14 (App Router), React, and Tailwind CSS. Create pages, reusable components, manage layout, and handle client-side state and data fetching.
---

# Frontend Development Skill

## Core Responsibilities

1.  **Next.js App Router Architecture**: Build the application structure using the `/app` directory, defining pages, layouts, loading states, and error boundaries.
2.  **Component Design & Development**: Create reusable, accessible, and performant React components (both server and client components) using TypeScript.
3.  **Styling & Theming**: Implement responsive and consistent visual designs using **Tailwind CSS** utility classes.
4.  **Client-Side State & Data Management**: Handle UI state with React hooks and manage server data fetching with Next.js APIs (`fetch`, `useEffect`, or libraries like TanStack Query).
5.  **Integration**: Connect the UI to the backend API and authentication services (Better Auth).

## Instructions

### 1. Next.js App Router Structure

Use the App Router (`/app`) for file-based routing. Key file conventions:
*   `app/page.tsx`: The main page for the route (`/`).
*   `app/layout.tsx`: The root layout that wraps all pages.
*   `app/loading.tsx`: An automatically displayed loading UI.
*   `app/dashboard/page.tsx`: The page for the `/dashboard` route.

**Example Root Layout (`app/layout.tsx`):**
```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthProvider } from '@/components/providers/AuthProvider'; // For auth state

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App - Phase II',
  description: 'A full-stack todo application',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-gray-900`}>
        <AuthProvider>
          <main className="min-h-screen">
            {/* A common header/navbar could go here */}
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
```

### 2. Building Reusable Components

Create components in an organized components/ directory. Use TypeScript interfaces for props.

Example: A Task Item Component (components/TaskItem.tsx):

```tsx
'use client'; // Mark as a Client Component if using interactivity

import { TaskPublic } from '@/schemas/task'; // Import the backend schema type
import { useState } from 'react';

interface TaskItemProps {
  task: TaskPublic;
  onToggleComplete: (taskId: number, completed: boolean) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

export default function TaskItem({ task, onToggleComplete, onDelete }: TaskItemProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleToggle = async () => {
    setIsLoading(true);
    await onToggleComplete(task.id, !task.completed);
    setIsLoading(false);
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow border border-gray-200">
      <div className="flex items-center space-x-3">
        <button
          onClick={handleToggle}
          disabled={isLoading}
          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300'}`}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && '✓'}
        </button>
        <div>
          <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-600">{task.description}</p>
          )}
        </div>
      </div>
      <button
        onClick={() => onDelete(task.id)}
        disabled={isLoading}
        className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
      >
        Delete
      </button>
    </div>
  );
}
```

### 3. Styling with Tailwind CSS

Use Tailwind's utility classes directly in your JSX for rapid, responsive styling.

Responsive Design: Use prefixes like sm:, md:, lg:.

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

Consistency: Define reusable styles in globals.css or use Tailwind's @apply directive for custom components.

Hover & Focus States: Use state variants like hover:, focus:.

```tsx
<button className="bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 ...">
```

### 4. Data Fetching & API Communication

Implement functions to communicate with your FastAPI backend. Manage loading and error states.

Example API Client Utility (lib/api.ts):

```tsx
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  // In a real app, get the token from your auth context/provider
  const token = localStorage.getItem('auth_token'); // Example

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

// Task-specific API calls
export const taskApi = {
  getAll: () => apiClient<TaskPublic[]>('/api/tasks'),
  create: (taskData: TaskCreate) => apiClient<TaskPublic>('/api/tasks', { method: 'POST', body: JSON.stringify(taskData) }),
  update: (taskId: number, updates: Partial<TaskPublic>) =>
    apiClient<TaskPublic>(`/api/tasks/${taskId}`, { method: 'PUT', body: JSON.stringify(updates) }),
  delete: (taskId: number) => apiClient(`/api/tasks/${taskId}`, { method: 'DELETE' }),
};
```

### 5. Authentication Integration (Better Auth)

Integrate the Better Auth library for managing user sessions.

Example Auth Context/Provider (components/providers/AuthProvider.tsx):

```tsx
'use client';
import { createContext, useContext, useEffect, useState } from 'react';
import { betterAuth } from 'better-auth'; // Hypothetical import

const auth = betterAuth({
  plugins: [/* JWT plugin config */],
});

interface AuthContextType {
  user: any | null;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    // Check for existing session on mount
    const checkSession = async () => {
      const session = await auth.getSession();
      if (session) setUser(session.user);
    };
    checkSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    const { data, error } = await auth.signIn.email({ email, password });
    if (error) throw error;
    setUser(data.user);
    // Store the token (Better Auth should handle this)
    localStorage.setItem('auth_token', data.token);
  };

  const signOut = async () => {
    await auth.signOut();
    setUser(null);
    localStorage.removeItem('auth_token');
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

## Best Practices

Server vs. Client Components: Default to Server Components for better performance. Use 'use client'; only when you need interactivity, state, or browser APIs.

Type Safety: Use TypeScript strictly. Share types (like TaskPublic) between frontend and backend if possible.

Accessibility (a11y): Use semantic HTML (<button>, <nav>), provide ARIA labels, and ensure keyboard navigation works.

Loading States: Always show loading indicators (skeletons, spinners) during data fetching.

Error Boundaries: Use error.tsx files to gracefully catch and display runtime errors in parts of your UI.

Optimistic Updates: For a smooth UX, update the UI immediately upon user action (e.g., toggling a task) before confirming with the server, then sync state afterward.

### Example Page Structure

A Dashboard Page (app/dashboard/page.tsx):

```tsx
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';

export default function DashboardPage() {
  // This is a Server Component. It can fetch data directly.
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Your Todo Dashboard</h1>
        <p className="text-gray-600">Manage your tasks efficiently.</p>
      </header>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Main Task List */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">My Tasks</h2>
          <TaskList />
        </div>

        {/* Sidebar for adding tasks */}
        <div className="lg:col-span-1">
          <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
          <div className="bg-white p-6 rounded-xl shadow">
            <TaskForm />
          </div>
        </div>
      </div>
    </div>
  );
}
```
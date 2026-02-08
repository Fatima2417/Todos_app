// frontend/lib/types.ts
// Define TypeScript interfaces matching backend API

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string; // ISO date string
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreateInput {
  title: string;
  description?: string;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Additional types for API responses if needed
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
// frontend/lib/tasks-query.ts
// TanStack Query (React Query) hooks for task operations

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from './api-client';
import { Task, TaskCreateInput, TaskUpdateInput } from './types';

// Query keys for cache management
const TASKS_QUERY_KEY = 'tasks';
const TASK_QUERY_KEY = 'task';

/**
 * Hook to fetch all tasks for a specific user
 */
export const useTasks = (user_id: string, completedFilter?: boolean | null) => {
  const queryKey: any[] = [TASKS_QUERY_KEY, user_id];
  if (completedFilter !== undefined && completedFilter !== null) {
    queryKey.push({ completed: completedFilter });
  }
  
  return useQuery({
    queryKey,
    queryFn: async () => {
      const params = completedFilter !== undefined && completedFilter !== null
        ? `?completed=${completedFilter}`
        : '';
      return apiClient<Task[]>(`/api/v1/${user_id}/tasks${params}`);
    },
    enabled: !!user_id,
  });
};

/**
 * Hook to fetch a single task by ID
 */
export const useTask = (user_id: string, task_id: number) => {
  return useQuery({
    queryKey: [TASK_QUERY_KEY, task_id, user_id],
    queryFn: async () => {
      return apiClient<Task>(`/api/v1/${user_id}/tasks/${task_id}`);
    },
    enabled: !!user_id && !!task_id,
  });
};

/**
 * Hook to create a new task
 */
export const useCreateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ user_id, taskData }: { user_id: string; taskData: TaskCreateInput }) => {        
      return apiClient.post<Task>(`/api/v1/${user_id}/tasks`, taskData);
    },
    // Optimistic update
    onMutate: async (variables) => {
      await queryClient.cancelQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
      const previousTasks = queryClient.getQueryData<Task[]>([TASKS_QUERY_KEY, variables.user_id]);

      if (previousTasks) {
        const optimisticTask: Task = {
          id: Math.random(), // Temporary ID
          title: variables.taskData.title,
          description: variables.taskData.description || null,
          completed: false,
          user_id: variables.user_id,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        queryClient.setQueryData<Task[]>(
          [TASKS_QUERY_KEY, variables.user_id],
          [optimisticTask, ...previousTasks]
        );
      }

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData([TASKS_QUERY_KEY, variables.user_id], context.previousTasks);
      }
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
    },
  });
};

/**
 * Hook to update an existing task
 */
export const useUpdateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      user_id,
      task_id,
      taskData
    }: {
      user_id: string;
      task_id: number;
      taskData: TaskUpdateInput
    }) => {
      return apiClient.put<Task>(`/api/v1/${user_id}/tasks/${task_id}`, taskData);
    },
    // Optimistic update
    onMutate: async (variables) => {
      await queryClient.cancelQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
      const previousTasks = queryClient.getQueryData<Task[]>([TASKS_QUERY_KEY, variables.user_id]);

      if (previousTasks) {
        queryClient.setQueryData<Task[]>(
          [TASKS_QUERY_KEY, variables.user_id],
          previousTasks.map((task) =>
            task.id === variables.task_id ? { ...task, ...variables.taskData } : task
          )
        );
      }

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData([TASKS_QUERY_KEY, variables.user_id], context.previousTasks);
      }
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
      queryClient.invalidateQueries({ queryKey: [TASK_QUERY_KEY, variables.task_id, variables.user_id] });
    },
  });
};

/**
 * Hook to toggle task completion
 */
export const useToggleTaskCompletion = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      user_id,
      task_id,
      completed
    }: {
      user_id: string;
      task_id: number;
      completed: boolean
    }) => {
      return apiClient.patch<Task>(`/api/v1/${user_id}/tasks/${task_id}/complete`, {});
    },
    // Optimistic update
    onMutate: async (variables) => {
      // Cancel any outgoing refetches (so they don't overwrite our optimistic update)
      await queryClient.cancelQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });

      // Snapshot the previous value
      const previousTasks = queryClient.getQueryData<Task[]>([TASKS_QUERY_KEY, variables.user_id]);

      // Optimistically update to the new value
      if (previousTasks) {
        queryClient.setQueryData<Task[]>(
          [TASKS_QUERY_KEY, variables.user_id],
          previousTasks.map((task) =>
            task.id === variables.task_id ? { ...task, completed: variables.completed } : task
          )
        );
      }

      return { previousTasks };
    },
    // If the mutation fails, use the context returned from onMutate to roll back
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData([TASKS_QUERY_KEY, variables.user_id], context.previousTasks);
      }
    },
    // Always refetch after error or success:
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
      queryClient.invalidateQueries({ queryKey: [TASK_QUERY_KEY, variables.task_id, variables.user_id] });
    },
  });
};

/**
 * Hook to delete a task
 */
export const useDeleteTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ user_id, task_id }: { user_id: string; task_id: number }) => {
      return apiClient.delete<null>(`/api/v1/${user_id}/tasks/${task_id}`);
    },
    // Optimistic update
    onMutate: async (variables) => {
      await queryClient.cancelQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
      const previousTasks = queryClient.getQueryData<Task[]>([TASKS_QUERY_KEY, variables.user_id]);

      if (previousTasks) {
        queryClient.setQueryData<Task[]>(
          [TASKS_QUERY_KEY, variables.user_id],
          previousTasks.filter((task) => task.id !== variables.task_id)
        );
      }

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData([TASKS_QUERY_KEY, variables.user_id], context.previousTasks);
      }
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: [TASKS_QUERY_KEY, variables.user_id] });
    },
  });
};

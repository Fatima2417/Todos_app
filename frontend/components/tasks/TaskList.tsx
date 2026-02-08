'use client';

import { Task } from '@/lib/types';
import { TaskItem } from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  userId: string;
  loading?: boolean;
  error?: string | null;
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (taskId: number) => void;
}

export function TaskList({
  tasks,
  userId,
  loading,
  error,
  onTaskUpdate,
  onTaskDelete
}: TaskListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="animate-pulse bg-gray-100 h-20 rounded-lg"></div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg bg-red-50 p-4 border border-red-100">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg border border-dashed border-gray-300">
        <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Pending Tasks Section */}
      {pendingTasks.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center">
            <span className="bg-indigo-100 text-indigo-700 px-2.5 py-0.5 rounded-full text-xs font-bold mr-2">
              {pendingTasks.length}
            </span>
            Pending Tasks
          </h2>
          <div className="space-y-3">
            {pendingTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                userId={userId}
                onEdit={onTaskUpdate}
                onDelete={onTaskDelete}
              />
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks Section */}
      {completedTasks.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center">
            <span className="bg-green-100 text-green-700 px-2.5 py-0.5 rounded-full text-xs font-bold mr-2">
              {completedTasks.length}
            </span>
            Completed
          </h2>
          <div className="space-y-3 opacity-80">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                userId={userId}
                onEdit={onTaskUpdate}
                onDelete={onTaskDelete}
              />
            ))}
          </div>
        </div>
      )}

      {pendingTasks.length === 0 && completedTasks.length > 0 && (
        <div className="text-center py-6 bg-green-50 rounded-lg border border-green-100">
          <p className="text-green-700 font-medium">✨ All caught up! All tasks completed.</p>
        </div>
      )}
    </div>
  );
}

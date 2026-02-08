'use client';

import { Task } from '@/lib/types';
import { Button } from '../ui/Button';

interface TaskFormProps {
  task?: Task;  // Optional for new task creation
  onSave: () => void;
  onCancel: () => void;
  isLoading?: boolean;
  value: {
    title: string;
    description: string;
  };
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

export function TaskForm({ task, onSave, onCancel, isLoading, value, onChange }: TaskFormProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={value.title}
          onChange={onChange}
          required
          disabled={isLoading}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
          placeholder="Task title"
        />
      </div>
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={value.description}
          onChange={onChange}
          rows={3}
          disabled={isLoading}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
          placeholder="Task description (optional)"
        />
      </div>
      <div className="flex space-x-3">
        <Button
          type="submit"
          loading={isLoading}
          className="bg-green-600 hover:bg-green-700 focus:ring-green-500"
        >
          {task ? 'Update Task' : 'Create Task'}
        </Button>
        <Button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          variant="secondary"
        >
          Cancel
        </Button>
      </div>
    </form>
  );
}
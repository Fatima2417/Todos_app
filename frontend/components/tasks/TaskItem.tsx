'use client';

import { Task } from '@/lib/types';
import { useToggleTaskCompletion } from '@/lib/tasks-query';

interface TaskItemProps {
  task: Task;
  userId: string;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onToggleComplete?: (taskId: number, completed: boolean) => void; // Optional if handled via mutation inside
}

// Since TaskItem is used in TaskList which is used in TaskDashboard, 
// and TaskDashboard provides the mutation handlers, we should use them.
// However, the user's snippet in the prompt showed:
// onDelete={(taskId) => deleteMutation.mutate(taskId)}
// which implies these are passed down.

export function TaskItem({ task, userId, onEdit, onDelete }: TaskItemProps) {
  const toggleMutation = useToggleTaskCompletion();

  const handleToggle = () => {
    toggleMutation.mutate({
      user_id: userId,
      task_id: task.id,
      completed: !task.completed
    });
  };

  return (
    <div 
      className={`group flex items-center justify-between p-4 rounded-lg border transition-all duration-200 ${
        task.completed 
          ? 'bg-green-50 border-green-200 shadow-sm' 
          : 'bg-white border-gray-200 hover:border-indigo-300 hover:shadow-md'
      }`}
    >
      <div className="flex items-center space-x-4 flex-1 min-w-0">
        <button
          onClick={handleToggle}
          disabled={toggleMutation.isPending}
          className={`flex-shrink-0 h-6 w-6 rounded-full border-2 flex items-center justify-center transition-colors ${
            task.completed
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-gray-300 text-transparent hover:border-green-500 hover:text-green-200'
          }`}
        >
          {task.completed && (
            <svg className="h-4 w-4 stroke-[3]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          )}
          {!task.completed && <div className="h-4 w-4" />}
        </button>
        
        <div className="flex-1 min-w-0">
          <h3 
            className={`text-sm font-medium truncate ${
              task.completed ? 'text-green-800 line-through' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p 
              className={`text-xs truncate ${
                task.completed ? 'text-green-600' : 'text-gray-500'
              }`}
            >
              {task.description}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-2 ml-4 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          onClick={() => onEdit(task)}
          className="p-1 text-gray-400 hover:text-indigo-600 rounded-full hover:bg-indigo-50 transition-colors"
          title="Edit task"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="p-1 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50 transition-colors"
          title="Delete task"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
}

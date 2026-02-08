'use client';

import { 
  useTasks, 
  useCreateTask, 
  useUpdateTask, 
  useDeleteTask, 
  useToggleTaskCompletion 
} from '@/lib/tasks-query';
import { TaskList } from '@/components/tasks/TaskList';
import { TaskForm } from '@/components/tasks/TaskForm';
import { useState } from 'react';
import { Task } from '@/lib/types';

interface TaskDashboardProps {
  userId: string;
}

export function TaskDashboard({ userId }: TaskDashboardProps) {
  const { data: tasks, isLoading, error } = useTasks(userId);
  
  const createTaskMutation = useCreateTask();
  const updateTaskMutation = useUpdateTask();
  const deleteTaskMutation = useDeleteTask();
  const toggleTaskMutation = useToggleTaskCompletion();

  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editTask, setEditTask] = useState<Task | null>(null);
  const [formValues, setFormValues] = useState({ title: '', description: '' });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormValues(prev => ({ ...prev, [name]: value }));
  };

  const handleSaveTask = async () => {
    try {
      if (editTask) {
        await updateTaskMutation.mutateAsync({
          user_id: userId,
          task_id: editTask.id,
          taskData: formValues
        });
      } else {
        await createTaskMutation.mutateAsync({
          user_id: userId,
          taskData: formValues
        });
      }
      // Only close and reset if successful (mutateAsync throws if it fails)
      handleCancelForm();
    } catch (err) {
      console.error('Error saving task:', err);
      // Form stays open for the user to try again or see the error
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTaskMutation.mutateAsync({ user_id: userId, task_id: taskId });
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    try {
      await toggleTaskMutation.mutateAsync({ 
        user_id: userId, 
        task_id: taskId, 
        completed 
      });
    } catch (err) {
      console.error('Error toggling task:', err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditTask(task);
    setFormValues({
      title: task.title,
      description: task.description || ''
    });
    setShowTaskForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancelForm = () => {
    setShowTaskForm(false);
    setEditTask(null);
    setFormValues({ title: '', description: '' });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <button
          onClick={() => {
            if (showTaskForm) {
              handleCancelForm();
            } else {
              setShowTaskForm(true);
            }
          }}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {showTaskForm ? 'Cancel' : 'Add New Task'}
        </button>
      </div>

      {showTaskForm && (
        <div className="mb-8 p-6 bg-white rounded-lg shadow border border-gray-100">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">
            {editTask ? 'Edit Task' : 'Create New Task'}
          </h2>
          <TaskForm
            task={editTask || undefined}
            onSave={handleSaveTask}
            onCancel={handleCancelForm}
            isLoading={createTaskMutation.isPending || updateTaskMutation.isPending}
            value={formValues}
            onChange={handleInputChange}
          />
          {(createTaskMutation.isError || updateTaskMutation.isError) && (
            <p className="mt-2 text-red-600 text-sm">
              Error saving task: {((createTaskMutation.error || updateTaskMutation.error) as Error)?.message}
            </p>
          )}
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-10">
          <p className="text-gray-600">Loading your tasks...</p>
        </div>
      ) : error ? (
        <div className="text-center py-10">
          <p className="text-red-600 font-medium">Error loading tasks: {(error as Error).message}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 text-indigo-600 hover:text-indigo-500 underline"
          >
            Retry
          </button>
        </div>
      ) : tasks && tasks.length > 0 ? (
        <TaskList
          tasks={tasks}
          userId={userId}
          loading={isLoading}
          error={null}
          onTaskUpdate={handleEditTask}
          onTaskDelete={handleDeleteTask}
        />
      ) : (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
          <div className="mt-6">
            <button
              onClick={() => setShowTaskForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Create your first task
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

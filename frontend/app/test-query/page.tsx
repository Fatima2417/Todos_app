'use client';

import { useTasks } from '@/lib/tasks-query';
import { useState } from 'react';

export default function TestQueryPage() {
  const [userId, setUserId] = useState('test-user-123');
  const { data, isLoading, error, refetch } = useTasks(userId);
  
  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">React Query Test Page</h1>
      
      <div className="mb-6 flex gap-2">
        <input 
          type="text" 
          value={userId} 
          onChange={(e) => setUserId(e.target.value)}
          className="border p-2 rounded flex-grow"
          placeholder="Enter User ID"
        />
        <button 
          onClick={() => refetch()}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Refetch
        </button>
      </div>

      {isLoading && (
        <div className="p-4 bg-blue-50 text-blue-700 rounded">
          Loading tasks for {userId}...
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded mb-4">
          Error: {error.message}
        </div>
      )}

      {data && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Tasks ({data.length})</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
      
      {!isLoading && !data && !error && (
        <p className="text-gray-500">Enter a user ID to fetch tasks.</p>
      )}
    </div>
  );
}

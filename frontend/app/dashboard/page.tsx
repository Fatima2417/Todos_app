'use client';

import { useAuth } from '@/hooks/useAuth';
import { TaskDashboard } from '@/components/tasks/TaskDashboard';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!user && typeof window !== 'undefined') {
      router.push('/login');
    }
  }, [user, router]);

  if (!user) {
    return <div>Please log in</div>;
  }

  return <TaskDashboard userId={user.id} />;
}

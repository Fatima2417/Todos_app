import { API_BASE_URL, API_ENDPOINTS } from '@/lib/config';
import { NextResponse } from 'next/server';

export async function GET() {
  const testResults: any = {
    timestamp: new Date().toISOString(),
    config: {
      API_BASE_URL,
      SIGN_IN_ENDPOINT: API_ENDPOINTS.SIGN_IN,
    },
    checks: [],
  };

  try {
    // 1. Check health endpoint
    const healthStart = Date.now();
    const healthResp = await fetch(`${API_BASE_URL}/health`, { cache: 'no-store' });
    const healthDuration = Date.now() - healthStart;
    
    testResults.checks.push({
      name: 'Backend Health Check',
      url: `${API_BASE_URL}/health`,
      status: healthResp.status,
      ok: healthResp.ok,
      duration: `${healthDuration}ms`,
    });

    // 2. Check Auth Endpoint (Dry run / just see if it responds)
    const authStart = Date.now();
    const authResp = await fetch(API_ENDPOINTS.SIGN_IN, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com', password: 'password' }),
      cache: 'no-store'
    });
    const authDuration = Date.now() - authStart;

    testResults.checks.push({
      name: 'Auth API Connectivity',
      url: API_ENDPOINTS.SIGN_IN,
      status: authResp.status,
      ok: authResp.status !== 404, // 401/400 is fine, means it reached the code
      duration: `${authDuration}ms`,
    });

  } catch (error: any) {
    testResults.error = {
      message: error.message,
      stack: error.stack,
    };
  }

  return NextResponse.json(testResults);
}

/**
 * Centralized API configuration
 */

// Use process.env.NEXT_PUBLIC_API_URL if defined, fallback to localhost for development
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  SIGN_IN: `${API_BASE_URL}/auth/sign-in/email`,
  SIGN_UP: `${API_BASE_URL}/auth/sign-up/email`,
  SIGN_OUT: `${API_BASE_URL}/auth/sign-out`,
  TASKS: `${API_BASE_URL}/api/v1`,
  CHAT: `${API_BASE_URL}/api/chat`,
};

// Log configuration in development mode only
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  console.log('API Base URL configured as:', API_BASE_URL);
}
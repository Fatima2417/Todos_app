// frontend/lib/simple-auth.ts
// Simple authentication system that works with our FastAPI backend

// Store auth state in localStorage
const AUTH_STORAGE_KEY = 'todo-app-auth';

export interface AuthUser {
  id: string;
  email: string;
  name?: string;
}

export interface AuthState {
  user: AuthUser | null;
  token: string | null;
}

export const getStoredAuth = (): AuthState => {
  if (typeof window === 'undefined') {
    return { user: null, token: null };
  }
  
  const stored = localStorage.getItem(AUTH_STORAGE_KEY);
  return stored ? JSON.parse(stored) : { user: null, token: null };
};

export const setStoredAuth = (auth: AuthState) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(auth));
  }
};

export const clearStoredAuth = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(AUTH_STORAGE_KEY);
  }
};

export const signup = async (email: string, password: string, name?: string) => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/sign-up/email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Signup failed');
  }

  const data = await response.json();
  
  // Store the user and token
  const authState: AuthState = {
    user: { id: data.user.id, email: data.user.email, name: name || email.split('@')[0] },
    token: data.access_token
  };
  
  setStoredAuth(authState);
  return authState;
};

export const login = async (email: string, password: string) => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/sign-in/email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  const data = await response.json();
  
  // Store the user and token
  const authState: AuthState = {
    user: { id: data.user.id, email: data.user.email, name: email.split('@')[0] },
    token: data.access_token
  };
  
  setStoredAuth(authState);
  return authState;
};

export const logout = () => {
  clearStoredAuth();
};

export const getCurrentUser = (): AuthUser | null => {
  const auth = getStoredAuth();
  return auth.user;
};

export const getAuthToken = (): string | null => {
  const auth = getStoredAuth();
  return auth.token;
};

export const isAuthenticated = (): boolean => {
  return !!getCurrentUser();
};
# Quickstart Guide: JWT Authentication Bridge for Todo Web App

## Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.11+ for FastAPI backend
- Better Auth compatible environment
- PyJWT library installed
- Environment variable: `BETTER_AUTH_SECRET`

## Installation

### Frontend Setup
1. Install Better Auth with JWT plugin:
   ```bash
   npm install @better-auth/react @better-auth/client
   ```
2. Configure Better Auth with JWT plugin in your Next.js app
3. Set up auth context to retrieve JWT tokens after login

### Backend Setup
1. Install required dependencies:
   ```bash
   pip install fastapi pyjwt python-decouple
   ```
2. Create auth handler module with JWT validation functions
3. Set up FastAPI dependency for user validation

## Environment Configuration
Set the shared secret in both frontend and backend environments:
```bash
BETTER_AUTH_SECRET="your-super-secret-key-here"
```

## Basic Implementation Steps

### 1. Create JWT Validation Utility (Backend)
- Create `auth_handler.py` with `decode_jwt()` function
- Implement signature verification using shared secret
- Add expiration validation

### 2. Create FastAPI Dependency
- Create `get_current_user` dependency
- Extract token from Authorization header
- Validate token and return user identity
- Raise 401 on invalid tokens

### 3. Secure API Endpoints
- Add `get_current_user` dependency to protected endpoints
- Remove user_id from path parameters where possible
- Use user identity for database query filtering

### 4. Frontend API Client
- Create API utility that attaches JWT to requests
- Implement token retrieval after successful login
- Handle 401 responses appropriately

## Testing the Setup
1. Register a user through the frontend
2. Verify JWT token is received and stored
3. Make API request with Authorization header
4. Confirm backend validates token and returns user data
5. Test invalid token rejection (401 responses)
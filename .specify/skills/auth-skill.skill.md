---
name: auth-skill
description: Implement secure user authentication flows including Signup, Signin, password hashing, JWT tokens, and Better Auth integration for full-stack applications.
---

# Authentication Implementation Skill

## Core Responsibilities

1. **User Registration (Signup)**
   - Collect email, password, and basic user info
   - Validate input (email format, password strength)
   - Hash passwords using industry-standard algorithms
   - Create user record in database
   - Return appropriate success/error responses

2. **User Authentication (Signin)**
   - Verify email/password credentials
   - Compare hashed passwords securely
   - Generate session tokens or JWTs
   - Set secure HTTP-only cookies if applicable
   - Handle "remember me" functionality

3. **Password Security**
   - Always hash passwords before storage (never store plaintext)
   - Use bcrypt or Argon2 with appropriate work factors
   - Implement password reset flows with secure tokens
   - Enforce password complexity requirements

4. **JWT Token Management**
   - Generate secure JWTs with appropriate claims (user_id, email, roles)
   - Set proper expiration times (short for access tokens, longer for refresh)
   - Implement token refresh mechanisms
   - Validate token signatures and expiration
   - Handle token blacklisting/revocation when needed

5. **Better Auth Integration**
   - Configure Better Auth provider in Next.js application
   - Set up JWT plugin for token generation
   - Implement authentication hooks and components
   - Handle social auth providers if required
   - Manage session state across the frontend

## Implementation Instructions

### Frontend (Next.js with Better Auth)

```typescript
// 1. Configure Better Auth with JWT
import { betterAuth } from "better-auth";
import { jwtPlugin } from "better-auth/plugins";

const auth = betterAuth({
  plugins: [jwtPlugin({ secret: process.env.BETTER_AUTH_SECRET! })],
  // ... other configuration
});

// 2. Signup component implementation
export function SignupForm() {
  // Handle form submission, validation, and API calls
}

// 3. Signin component implementation
export function SigninForm() {
  // Handle login, token storage, and redirect
}

// 4. API client with JWT attachment
export function apiClient() {
  // Interceptor to attach token to all requests
  headers: { Authorization: `Bearer ${token}` }
}
```

### Backend (FastAPI with JWT Validation)

```python
# 1. JWT validation middleware
from fastapi import Request, HTTPException
import jwt

async def validate_jwt(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        request.state.user_id = payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 2. Password hashing utilities
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. Protected endpoint example
@app.get("/api/tasks")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id  # From middleware
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

## Best Practices

### Security
- Never store plaintext passwords - always use strong hashing
- Use HTTPS exclusively in production environments
- Set appropriate token expiration (e.g., 15-30 minutes for access tokens)
- Implement rate limiting on authentication endpoints
- Validate all inputs to prevent injection attacks
- Use HTTP-only cookies for token storage when possible

### User Experience
- Provide clear error messages without revealing security details
- Implement loading states during authentication processes
- Remember user sessions appropriately (balance security vs convenience)
- Support password recovery with secure reset flows
- Make authentication flows accessible (keyboard navigation, screen readers)

### Architecture
- Keep authentication logic separate from business logic
- Use environment variables for all secrets (never hardcode)
- Implement proper logging (without sensitive data)
- Support multiple authentication methods if needed (email/password, OAuth, etc.)
- Design stateless authentication where possible for scalability

## Common Flows

### Standard Email/Password Flow
1. User submits credentials → Validate input → Hash password → Create user → Generate JWT → Return token
2. User logs in → Verify credentials → Generate JWT → Return token → Store token client-side
3. User accesses protected resource → Attach token → Validate server-side → Return data

### Token Refresh Flow
- Access token expires → Client uses refresh token → Server validates refresh token → Issues new access token
- Refresh token expires → User must re-authenticate

### Password Reset Flow
- User requests reset → Generate secure token → Send email → User clicks link → Validate token → Allow password change

## Integration Notes
- Better Auth is a frontend library - backend must independently verify JWTs
- Shared secret must be identical in frontend (Better Auth config) and backend (JWT verification)
- User IDs in JWTs must match database user IDs for proper data isolation
- CORS must be configured to allow frontend-backend communication
- Environment variables should store: BETTER_AUTH_SECRET, DATABASE_URL, JWT_EXPIRATION

## Troubleshooting Common Issues
- "Invalid token" errors: Check shared secret matches, token expiration, algorithm compatibility
- CORS errors: Ensure backend allows requests from frontend origin
- User data mixing: Verify user_id extraction from JWT matches database queries
- Password mismatches: Confirm consistent hashing algorithms and salts
- Session persistence issues: Check token storage and attachment to requests
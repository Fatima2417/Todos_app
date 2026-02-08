# Data Model: JWT Authentication Bridge for Todo Web App

## JWT Token Structure

### Token Payload Claims
- **sub** (Subject): User ID string from Better Auth
- **iat** (Issued At): Unix timestamp of token creation
- **exp** (Expiration): Unix timestamp of token expiration
- **email** (Optional): User's email address

### Token Validation Properties
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: BETTER_AUTH_SECRET environment variable
- **Expiration**: 24 hours (configurable)

## User Session Representation

### Client-Side Session
- **userId**: Extracted from JWT token after successful login
- **accessToken**: JWT token string for API authorization
- **expiresAt**: Expiration timestamp for token refresh logic
- **isLoggedIn**: Boolean indicating authentication status

### Backend User Identity Object
- **id**: User ID from JWT token payload (primary identifier)
- **email**: User email from JWT token (for logging/tracking)
- **permissions**: User permissions derived from authentication (currently all users have equal permissions)

## API Request Structure

### Authenticated Request Headers
- **Authorization**: "Bearer {jwt_token}" format
- **Content-Type**: "application/json" for JSON APIs

### Protected Endpoint Parameters
- **user_id** (from token): User ID validated against JWT claim
- **user_object** (from dependency): Complete user identity object for business logic

## Security Validation Model

### Token Validation Process
1. Extract Authorization header
2. Verify "Bearer " prefix
3. Validate JWT signature using BETTER_AUTH_SECRET
4. Check token expiration
5. Extract and validate user_id from payload
6. Return user identity object or raise HTTPException(401)

### User Data Isolation Enforcement
- **Owner Check**: Verify that requested resource belongs to authenticated user
- **Filter Enforcement**: Apply user_id filter to all database queries
- **Access Control**: Reject requests where JWT user_id doesn't match requested resource owner
# Research Summary: JWT Authentication Bridge for Todo Web App

## Decision: JWT Token Implementation
**Rationale**: Using PyJWT library in FastAPI backend to validate tokens issued by Better Auth. This approach provides cryptographic signature verification, which is stateless and scalable.
**Alternatives considered**:
- Manual JWT parsing and validation (security risks, maintenance burden)
- Database-based session lookup (violates stateless constraint, scalability issues)

## Decision: Better Auth Configuration
**Rationale**: Configuring Better Auth with JWT plugin to issue tokens that contain user ID in the payload. This enables seamless integration between frontend authentication and backend validation.
**Alternatives considered**:
- Custom JWT implementation (reinventing security, potential vulnerabilities)
- Alternative auth libraries (would not meet tech stack compliance requirement)

## Decision: Authorization Header Format
**Rationale**: Using standard `Authorization: Bearer <token>` header format for API requests. This is the RFC 6750 standard for OAuth 2.0 bearer tokens and is widely supported.
**Alternatives considered**:
- Custom header names (non-standard, integration complexity)
- Token in request body (insecure, non-standard practice)

## Decision: Shared Secret Management
**Rationale**: Using environment variable (BETTER_AUTH_SECRET) for the signing key in both Next.js and FastAPI applications. This keeps the secret secure and allows different values across environments.
**Alternatives considered**:
- Hardcoded secrets (security violation)
- Different secrets per service (breaks token validation)

## Decision: User Identification Method
**Rationale**: Extracting user ID exclusively from the validated JWT token payload, with validation against URL parameters to prevent authorization bypass. This makes the JWT the single source of truth for user identity.
**Alternatives considered**:
- Reading user ID from URL path only (vulnerable to authorization bypass)
- Database lookup for each request (violates stateless requirement, performance issues)

## Decision: FastAPI Dependency Injection
**Rationale**: Implementing JWT validation as a reusable FastAPI dependency (`get_current_user`) that can be injected into any endpoint. This promotes code reuse and consistent security enforcement.
**Alternatives considered**:
- Manual validation in each endpoint (code duplication, inconsistency risk)
- Middleware-based approach (less flexible for selective endpoint protection)

## Decision: Database Query Filtering
**Rationale**: Using the user ID extracted from the JWT token to filter all database queries at the service/db layer. This ensures data isolation between users at the persistence level.
**Alternatives considered**:
- Client-side filtering (security vulnerability)
- API-level filtering without db-level enforcement (potential bypass)
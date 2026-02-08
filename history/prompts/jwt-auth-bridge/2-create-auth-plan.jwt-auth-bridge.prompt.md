---
id: 2
title: create-auth-plan
stage: plan
date_iso: 2026-02-05
surface: agent
model: claude-opus-4-6
feature: jwt-auth-bridge
branch: 001-jwt-auth-bridge
user: Hp
command: sp.plan
labels: ["auth", "jwt", "plan", "security"]
links:
  spec: "../../specs/001-jwt-auth-bridge/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-jwt-auth-bridge/plan.md"
  - "specs/001-jwt-auth-bridge/research.md"
  - "specs/001-jwt-auth-bridge/data-model.md"
  - "specs/001-jwt-auth-bridge/quickstart.md"
  - "specs/001-jwt-auth-bridge/contracts/auth-contract.json"
tests_yaml: []
---

# Prompt Text
```
 for Authentication & User Security Flow
Project: Phase II - Todo Full-Stack Web App
Spec: P2-SPEC-1 (Authentication & User Security Flow)
Primary Agent: jwt-auth-specialist

1. Architecture Sketch & Data Flow
The system implements a stateless, token-based authentication flow. The frontend (Next.js) handles user login via Better Auth, which issues a JWT. This token is then used to authorize all requests to the protected FastAPI backend.

sequenceDiagram
    participant User
    participant Frontend (Next.js / Better Auth)
    participant Backend (FastAPI)
    participant Database (Neon)

    User->>Frontend: 1. Enters credentials (Login/Signup)
    Frontend->>Frontend: 2. Better Auth validates & creates session
    Frontend->>Frontend: 3. Better Auth JWT plugin issues token[citation:5]
    Frontend->>User: 4. Returns session & JWT token

    User->>Frontend: 5. Clicks "View My Tasks"
    Frontend->>Backend: 6. HTTP Request (GET /api/tasks)<br>Header: `Authorization: Bearer <JWT>`[citation:1]
    Backend->>Backend: 7. Validates JWT signature & extracts `user_id`
    Backend->>Database: 8. Query: `SELECT * FROM tasks WHERE user_id = ?`
    Database->>Backend: 9. Returns user's tasks
    Backend->>Frontend: 10. JSON response with tasks
    Frontend->>User: 11. Displays task list
2. Technical Decisions & Component Design
Decision Point	Options Considered	Chosen Approach & Rationale
Token Format & Library	Manual JWT handling, PyJWT library	Use PyJWT in FastAPI backend. It's a robust, standard library for signing and decoding JWTs, reducing custom code and potential security flaws.
Secret Management	Hardcoded secret, environment variables	Use environment variable (BETTER_AUTH_SECRET). This keeps the signing key secure, allows different values for development/production, and is required for Better Auth compatibility.
Token Validation Location	Database lookup on each request, cryptographic signature verification	Cryptographic signature verification only. JWTs are self-contained. The backend verifies the token's signature using the shared secret. This is stateless and scalable, aligning with the hackathon's constraint.
User Identity in Backend	Read user_id from URL path, read user_id from validated JWT	Extract user_id exclusively from the validated JWT token. The token payload is the single source of truth. The user_id in API paths, if present, must be validated against the JWT claim to prevent users from accessing other users' data.
Better Auth Client Setup	Basic auth, auth with JWT plugin	Configure Better Auth with the official JWT plugin. This provides the dedicated /token endpoint or client method to retrieve a JWT after login, which is essential for the backend to recognize the user.
3. Implementation Blueprint
This blueprint breaks down the work into actionable tasks for the jwt-auth-specialist and defines handoffs to other agents.

A. Frontend Auth Setup (Next.js / Better Auth)
Agent: jwt-auth-specialist (using Frontend Skill)

Tasks:

Install and configure Better Auth in the Next.js application.
Integrate the Better Auth JWT plugin. Configure it to include the user's id (and optionally email) in the token payload.
Create a client-side auth context or hook that, after login, retrieves the JWT token using auth.getToken() or from the /token endpoint.
Create an API client utility (e.g., lib/api.js) that automatically injects the JWT token into the Authorization: Bearer <token> header of every outgoing request to the FastAPI backend.
Deliverable: A working login form where, upon success, the application stores a JWT and can attach it to API calls.

B. Backend Auth Infrastructure (FastAPI)
Agent: jwt-auth-specialist (using Backend Skill)

Tasks:

Install python-jwt (PyJWT) and python-decouple for environment management.
Create an auth_handler.py module. Implement:
sign_jwt(user_id: str): (For reference/mocks; actual signing is done by Better Auth).
decode_jwt(token: str): Function to verify token signature and expiration using the BETTER_AUTH_SECRET.
Create a FastAPI dependency (e.g., get_current_user). This dependency will:
Extract the token from the Authorization header.
Call decode_jwt() to validate it.
Return the extracted user_id (and user object). If invalid, raise an HTTPException(status_code=401).
Deliverable: A reusable Depends(get_current_user) that can secure any endpoint.

C. Securing the Task Endpoints
Primary Agent: fastapi-backend-architect

Collaboration: jwt-auth-specialist provides the get_current_user dependency.

Tasks:

Update all task-related API endpoints (from the spec: GET /api/{user_id}/tasks, POST /api/{user_id}/tasks, etc.).
Add the get_current_user dependency to each endpoint.
Remove user_id from the path parameters. The user is identified by the token. Endpoints should become /api/tasks, /api/tasks/{id}, etc.
Modify all service and database logic to use the user_id from get_current_user for filtering (WHERE clauses) and ownership checks. This enforces user data isolation.
Deliverable: All core API endpoints are protected and respect data boundaries.

D. Database Schema Preparation
Agent: neon-database-operator

Prerequisite: Must wait for the User model definition from the frontend/backend auth setup.

Tasks:

Define the users table schema. The id field should be a String type to match the user ID provided by Better Auth.
Ensure the tasks table has a foreign key (user_id) linking to users.id.
Create an index on tasks.user_id for performant queries.
Deliverable: Database schema ready to store users and user-owned tasks.

4. Testing & Validation Strategy
Positive Flow: Test that logging in on the frontend allows successful calls to GET /api/tasks, which returns only that user's tasks.

Security Validation:

Token Missing: Call an API without a token -> Must return 401.

Invalid Token: Call an API with a malformed token -> Must return 401.

Ownership Test: With two users (A & B), ensure a task created by User A is never visible or modifiable by User B via the API.

Success Handoff Criteria: The authentication system is considered complete when the fastapi-backend-architect can successfully build a GET /api/tasks endpoint that uses the get_current_user dependency and returns correctly filtered data.

5. Integration Notes & Handoff
This spec is a prerequisite for P2-SPEC-2 (Database) and P2-SPEC-3 (API & Business Logic). The neon-database-operator needs the User model details, and the fastapi-backend-architect requires the completed get_current_user dependency to build secure business logic.

The key outcome is a shared, validated user_id that flows from the frontend token through the backend dependency and into every database query, forming the foundation for a secure, multi-user application.
```

# Response Text
Created the implementation plan for the JWT Authentication Bridge feature, including:
- Filled the plan template with specific details for the JWT auth system
- Completed research.md with key decisions on JWT implementation, Better Auth configuration, token format, secret management, user identification, FastAPI dependency injection, and database filtering
- Created data-model.md defining JWT structure, user session representation, API request structure, and security validation model
- Created quickstart.md with prerequisites, installation steps, configuration, and basic implementation steps
- Created auth-contract.json defining the API contract for authentication endpoints
- Updated agent context to include new technologies (Python 3.11, Node.js 18+, Better Auth, FastAPI, PyJWT, SQLModel, Neon PostgreSQL)
- Ensured all constitutional requirements were met (agentic specialization, security by default, clean architecture, tech stack compliance)

# Outcome
Successfully created a comprehensive implementation plan for the JWT authentication bridge that connects Next.js frontend with FastAPI backend using Better Auth, with all required documentation and contract definitions.

# Evaluation
The implementation plan meets all requirements with proper research, data modeling, and architectural decisions that align with the project constitution and security requirements. The plan properly defines the division of work among specialized agents and establishes the foundation for secure user data isolation.
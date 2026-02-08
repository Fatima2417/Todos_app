# Tasks: JWT Authentication Bridge for Todo Web App

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (Secure User Registration and Login) with minimal auth infrastructure
**Delivery Order**: Build foundational auth system first, then integrate with each user story incrementally
**Parallel Opportunities**: Backend JWT utility and Frontend auth configuration can be developed simultaneously

---

## Phase 1: Project Setup & Environment Configuration

### Goal
Initialize the monorepo structure and configure environment variables for both frontend and backend auth systems.

### Independent Test
Verify that project structure is created and environment variables are accessible in both frontend and backend.

### Tasks

- [x] T001 Create frontend directory structure: `/frontend`, `/frontend/src`, `/frontend/app`, `/frontend/lib`
- [x] T002 Create backend directory structure: `/backend`, `/backend/src`, `/backend/src/auth`, `/backend/src/dependencies`, `/backend/src/utils`
- [x] T003 Create shared environment files: `/frontend/.env.local`, `/backend/.env`
- [x] T004 [P] Configure frontend env vars: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET in `/frontend/.env.local`
- [x] T005 [P] Configure backend env vars: DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM in `/backend/.env`
- [x] T006 Initialize frontend package.json with Next.js, Better Auth dependencies
- [x] T007 Initialize backend requirements.txt with FastAPI, PyJWT, python-decouple dependencies

---

## Phase 2: Foundational Auth Infrastructure

### Goal
Build the core authentication utilities that will be shared across all user stories.

### Independent Test
Verify that JWT utilities can encode and decode tokens with the shared secret.

### Tasks

- [x] T008 [P] [US1] Install Better Auth with JWT plugin in frontend (`@better-auth/react`, `@better-auth/client`)
- [x] T009 [P] [US1] Install PyJWT and python-decouple in backend (`pip install pyjwt python-decouple`)
- [x] T010 [P] [US1] Create Better Auth configuration in `/frontend/lib/auth.ts`
- [x] T011 [US1] Create JWT utility functions in `/backend/src/auth/jwt.py`
- [x] T012 [US1] Create get_current_user dependency in `/backend/src/dependencies.py`
- [x] T013 [US1] Implement token validation with BETTER_AUTH_SECRET in JWT utility
- [ ] T014 [US1] Test token creation and validation with shared secret

---

## Phase 3: User Story 1 - Secure User Registration and Login (Priority: P1)

### Goal
Enable users to register for an account and log in using email and password via Better Auth.

### Independent Test
The registration and login flows can be fully tested independently by registering a new user, logging in, and verifying that the user session is established and maintained properly.

### Acceptance Tests
- Given an unregistered user visits the app, when they register with valid credentials, then an account is created and they are logged in
- Given a registered user visits the app, when they enter valid credentials, then they are authenticated and granted access to their private todo items
- Given a registered user attempts to login with invalid credentials, when they submit the form, then authentication fails and an appropriate error is displayed

### Implementation Tasks

- [x] T015 [P] [US1] Create login page component in `/frontend/app/login/page.tsx`
- [x] T016 [P] [US1] Create signup page component in `/frontend/app/signup/page.tsx`
- [ ] T017 [US1] Implement signup form with email/password validation in signup page
- [ ] T018 [US1] Implement login form with email/password validation in login page
- [ ] T019 [US1] Connect signup form to Better Auth client (signUp.email())
- [ ] T020 [US1] Connect login form to Better Auth client (signIn.email())
- [ ] T021 [US1] Implement error handling for authentication failures
- [ ] T022 [US1] Store session information after successful authentication
- [ ] T023 [US1] Create authentication context to manage user state in `/frontend/contexts/AuthContext.jsx`

---

## Phase 4: User Story 2 - Secure API Access with JWT Token (Priority: P1)

### Goal
Enable authenticated users to perform todo operations via API calls with JWT token authentication.

### Independent Test
Can be tested by simulating API requests with and without valid JWT tokens to verify authentication requirements are enforced.

### Acceptance Tests
- Given an authenticated user makes an API request, when the request includes a valid JWT token, then the request is processed and the user receives appropriate data
- Given an unauthenticated user makes an API request, when the request lacks a JWT token, then the request is rejected with a 401 Unauthorized response
- Given a user makes an API request, when the request includes an invalid/expired JWT token, then the request is rejected with a 401 Unauthorized response

### Implementation Tasks

- [x] T024 [P] [US2] Create API client utility in `/frontend/lib/api.js`
- [x] T025 [US2] Implement JWT token attachment to API requests in API client
- [x] T026 [US2] Create test endpoint GET /api/test-auth in backend
- [x] T027 [US2] Apply get_current_user dependency to test endpoint
- [ ] T028 [US2] Test endpoint returns 401 for unauthenticated requests
- [ ] T029 [US2] Create API call in frontend to test endpoint with JWT token
- [ ] T030 [US2] Verify authenticated requests are accepted and unauthenticated rejected

---

## Phase 5: User Story 3 - User Data Isolation (Priority: P1)

### Goal
Ensure users can only view and modify their own data by validating JWT user ID against request parameters.

### Independent Test
Can be tested by attempting to access another user's data using a valid JWT from a different user to verify authorization is properly enforced.

### Acceptance Tests
- Given a user with valid JWT token makes a request for their own data, when the JWT user ID matches the request parameter user ID, then the request succeeds and returns the appropriate data
- Given a user with valid JWT token makes a request for another user's data, when the JWT user ID does not match the request parameter user ID, then the request is rejected with an appropriate error
- Given a user retrieves their todo list, when the API filters results by the authenticated user ID, then only the user's own todos are returned

### Implementation Tasks

- [x] T031 [US3] Enhance get_current_user dependency to validate user ID against request path
- [x] T032 [US3] Create validate_user_param dependency to compare JWT user ID with path parameter
- [x] T033 [US3] Implement user ID validation for test endpoint to ensure JWT matches path param
- [x] T034 [US3] Create database query filtering logic by user ID
- [x] T035 [US3] Test user isolation by attempting to access another user's data with valid token
- [x] T036 [US3] Ensure all API endpoints validate user authorization before processing

---

## Phase 6: Integration & Testing

### Goal
Complete end-to-end testing of the authentication bridge and prepare for handoff to database team.

### Independent Test
Complete integration test demonstrating the full authentication flow from signup to API access with proper user isolation.

### Tasks

- [x] T037 [US3] Create comprehensive integration test for full auth flow
- [x] T038 [US3] Test user registration → login → JWT retrieval → API access
- [x] T039 [US3] Test user data isolation with multiple user accounts
- [x] T040 [US3] Verify all FR requirements are satisfied
- [x] T041 [US3] Document auth bridge for P2-SPEC-2 handoff
- [x] T042 [US3] Update CLAUDE.md to confirm auth bridge is operational
- [x] T043 [US3] Create README documentation for auth implementation

---

## Dependencies

### User Story Completion Order
- Foundational Auth Infrastructure (Phase 2) → User Story 1 (Phase 3) → User Story 2 (Phase 4) → User Story 3 (Phase 5)

### Task Dependencies
- T008-T012 depend on T001-T007 (Environment setup)
- T015-T023 depend on T008-T014 (Auth infrastructure for US1)
- T024-T030 depend on T015-T023 (US1 for US2)
- T031-T036 depend on T024-T030 (US2 for US3)
- T037-T043 depend on T031-T036 (US3 for integration)

---

## Parallel Execution Examples

### Per User Story
- **User Story 1**: T015 and T016 can be developed in parallel (login and signup pages)
- **User Story 2**: T024 and T026 can be developed in parallel (frontend API client and backend test endpoint)
- **User Story 3**: T031 and T034 can be developed in parallel (validation and database logic)
# Tasks: RESTful API & Business Logic for Todo Web App

**Feature**: RESTful API & Business Logic for Todo Web App
**Branch**: 001-rest-api-logic
**Generated**: 2026-02-06
**Input**: `/specs/001-rest-api-logic/spec.md` and `/specs/001-rest-api-logic/plan.md`

## Implementation Strategy

The REST API implementation will follow a phased approach focusing on:
1. Setting up the FastAPI application infrastructure
2. Creating the Pydantic schemas for request/response validation
3. Building the service layer with business logic
4. Implementing the API endpoints with security validation
5. Validating the complete API functionality

The approach follows security-by-default principles with user_id validation and JWT token integration.

## Phase 1: Setup & Infrastructure

Initialize the backend API structure and install necessary dependencies for the API layer.

- [x] T001 Create backend API directory structure: `/backend/src/api`, `/backend/src/schemas`, `/backend/src/services`, `/backend/src/core`
- [x] T002 Create backend requirements file with FastAPI dependencies in `/backend/requirements.txt`
- [x] T003 Create main application file `/backend/app.py` with FastAPI instance
- [x] T004 Create core config file `/backend/src/core/config.py` for API settings

## Phase 2: Foundation - Schemas & Dependencies

Establish the foundational API components before implementing business logic.

- [x] T005 Create TaskCreate schema in `/backend/src/schemas/task.py`
- [x] T006 Create TaskUpdate schema in `/backend/src/schemas/task.py`
- [x] T007 Create TaskPublic schema in `/backend/src/schemas/task.py`
- [x] T008 [P] Create user dependency in `/backend/src/dependencies.py`
- [x] T009 [P] Create validation dependency for user path in `/backend/src/dependencies.py`
- [x] T010 Create API router in `/backend/src/api/routes/tasks.py`

## Phase 3: User Story 1 - Secure Task Management API [P1]

Implement the foundational ability to securely manage tasks through the API with proper user isolation.

**Goal**: Enable users to perform all basic operations (Add, Delete, Update, View, Mark Complete) while ensuring data isolation.

**Independent Test Criteria**:
- Users can perform all basic operations on their tasks
- System only allows access to the authenticated user's tasks
- Security validation prevents cross-user access

**Acceptance Tests**:
- [ ] T011 [US1] Write test verifying user can create task
- [ ] T012 [US1] Write test verifying user cannot access another user's tasks

**Implementation Tasks**:
- [x] T013 [US1] Create API routes for listing tasks GET `/api/v1/{user_id}/tasks`
- [x] T014 [US1] Create API route for creating tasks POST `/api/v1/{user_id}/tasks`
- [x] T015 [US1] Create API route for getting specific task GET `/api/v1/{user_id}/tasks/{task_id}`
- [x] T016 [US1] Verify JWT authentication and user_id path validation works

## Phase 4: User Story 2 - Robust API Validation & Error Handling [P1]

Implement comprehensive validation and error handling for all API operations.

**Goal**: Ensure API provides consistent validation and clear error responses.

**Independent Test Criteria**:
- API endpoints validate all input using Pydantic models
- Appropriate HTTP status codes are returned for different scenarios
- Structured JSON error responses are provided

**Acceptance Tests**:
- [ ] T017 [US2] Write test for malformed request validation
- [ ] T018 [US2] Write test for unauthorized access response
- [ ] T019 [US2] Write test for non-existent task response

**Implementation Tasks**:
- [x] T020 [US2] Create API route for updating tasks PUT `/api/v1/{user_id}/tasks/{task_id}`
- [x] T021 [US2] Create API route for deleting tasks DELETE `/api/v1/{user_id}/tasks/{task_id}`
- [x] T022 [US2] Create API route for toggling completion PATCH `/api/v1/{user_id}/tasks/{task_id}/complete`
- [x] T023 [US2] Implement proper error handling with consistent JSON responses

## Phase 5: User Story 3 - Seamless System Integration [P2]

Integrate the API layer with authentication and database services to form a cohesive system.

**Goal**: Enable the API to connect authentication with data persistence while maintaining security.

**Independent Test Criteria**:
- API correctly extracts user identity from JWT tokens
- Path parameter validation ensures JWT user_id matches path parameter
- Database operations are performed through repository layer

**Acceptance Tests**:
- [ ] T024 [US3] Write integration test with JWT token validation
- [ ] T025 [US3] Write test verifying user_id path parameter validation

**Implementation Tasks**:
- [x] T026 [US3] Create task service in `/backend/src/services/task_service.py`
- [x] T027 [US3] Integrate service with repository functions from P2-SPEC-2
- [x] T028 [US3] Implement complete API flow validation with JWT and path checks

## Phase 6: Validation & Documentation

Validate that all functionality works as expected and provide proper documentation.

- [x] T029 Validate that all endpoints return correct HTTP status codes
- [x] T030 Test all error scenarios and ensure proper responses
- [x] T031 Verify the critical security rule is enforced across all endpoints
- [x] T032 Update CLAUDE.md to reflect operational API layer
- [x] T033 Document API endpoints for handoff to frontend development

## Dependencies

- T005-T007 must complete before T013-T022 (Schemas before routes)
- T008-T009 must complete before T013-T022 (Dependencies before routes)
- T001-T004 must complete before T013-T022 (Foundation before routes)
- Authentication layer (P2-SPEC-1) and database layer (P2-SPEC-2) must be available before T026-T028

## Parallel Execution Opportunities

- T005, T006, T007 can run in parallel (Task schemas)
- T008 and T009 can run in parallel (Dependencies)
- T011 and T012 can run in parallel (US1 tests)
- T017, T018, and T019 can run in parallel (US2 tests)
- T024 and T025 can run in parallel (US3 tests)
# Feature Specification: RESTful API & Business Logic for Todo Web App

**Feature Branch**: `001-rest-api-logic`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "RESTful API & Business Logic for Todo Web App

Target audience: The `fastapi-backend-architect` agent and the `nextjs-frontend-engineer` agent who will consume the API.
Focus: Define the core application layer. This includes building the FastAPI application structure, implementing all specified REST endpoints, defining Pydantic schemas for robust request/response validation, and orchestrating the business logic that connects the authentication and database layers.

Success criteria:
- A fully functional FastAPI application is running, with auto-generated interactive API documentation (Swagger UI/Redoc).
- All six REST endpoints (`GET /api/{user_id}/tasks`, `POST /api/{user_id}/tasks`, `GET /api/{user_id}/tasks/{id}`, `PUT /api/{user_id}/tasks/{id}`, `DELETE /api/{user_id}/tasks/{id}`, `PATCH /api/{user_id}/tasks/{id}/complete`) are implemented and secured.
- Each endpoint uses Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskPublic`) for validation and serialization.
- The **critical security rule** is enforced: the `user_id` extracted from the JWT token (via `get_current_user`) is used for all operations, and the `user_id` in the request path is validated against it.
- The business logic (service layer) correctly calls the corresponding CRUD functions from the `task_repository` (P2-SPEC-2).
- The API returns appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 422) and structured JSON error responses.

Constraints:
- Framework: Must use FastAPI. All endpoints must be defined using its decorators and dependency injection.
- Validation: Must use Pydantic models for all request bodies and response models. No manual validation.
- Security Integration: Must use the `get_current_user` dependency from P2-SPEC-1. Must implement path parameter validation to prevent user impersonation.
- Data Layer Integration: Must call functions from the `task_repository` module (P2-SPEC-2) for all database interactions. No raw SQL in routes.
- Structure: Must follow a clean architecture pattern (e.g., `routers/`, `schemas/`, `services/`, `dependencies/`).
- Spec-Driven: All implementation must be derived from specifications.

Not building:
- The authentication logic or JWT validation (owned by P2-SPEC-1).
- The database schema or raw CRUD operations (owned by P2-SPEC-2).
- The frontend user interface or components (owned by P2-SPEC-4).
- Any features beyond the five Basic Level operations (Add, Delete, Update, View, Mark Complete). No search, filter, sort, priorities, due dates, or recurring tasks.
- User registration/login API endpoints (handled by Better Auth on the frontend; backend only verifies tokens)."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST implement FastAPI application with Swagger UI and Redoc documentation
- **FR-002**: System MUST implement six REST endpoints: GET, POST, GET by ID, PUT, DELETE, PATCH for completion status
- **FR-003**: System MUST use Pydantic models for request/response validation and serialization
- **FR-004**: System MUST validate user_id from JWT token matches user_id in request path parameter
- **FR-005**: System MUST call functions from task_repository module for all database interactions
- **FR-006**: System MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 422)
- **FR-007**: System MUST return structured JSON error responses
- **FR-008**: System MUST enforce user data isolation through the security validation mechanism
- **FR-009**: System MUST follow clean architecture with separate routers, schemas, services, and dependencies modules
- **FR-010**: System MUST provide proper dependency injection for database sessions and user authentication

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item with properties like id, title, description, completion status, timestamps, and user ownership
- **TaskCreate**: Schema for validating new task creation requests with required fields and constraints
- **TaskUpdate**: Schema for validating task update requests with optional fields
- **TaskPublic**: Schema for serializing task responses for external consumption
- **Authentication Token**: JWT token containing user identity that is validated against request parameters

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fully functional FastAPI application is running with interactive API documentation available
- **SC-002**: All six specified REST endpoints are implemented and secured according to requirements
- **SC-003**: All API endpoints properly validate requests using Pydantic models and return correct responses
- **SC-004**: The critical security rule is enforced: user_id from JWT matches path parameter and operations are filtered accordingly
- **SC-005**: All database operations are performed through the repository layer without raw SQL in routes
- **SC-006**: API returns appropriate HTTP status codes and structured JSON error responses for all scenarios
- **SC-007**: The system follows clean architecture patterns with properly separated modules

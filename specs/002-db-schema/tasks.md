# Tasks: Database Schema & Operations for Todo Web App

**Feature**: Database Schema & Operations for Todo Web App
**Branch**: 002-db-schema
**Generated**: 2026-02-06
**Input**: `/specs/002-db-schema/spec.md` and `/specs/002-db-schema/plan.md`

## Implementation Strategy

The database layer implementation will follow a phased approach focusing on:
1. Setting up the Neon database infrastructure
2. Creating the SQLModel data models
3. Building the repository layer with secure CRUD operations
4. Integrating with the authentication system
5. Validating user data isolation

The approach follows security-by-default principles with user_id filtering mandatory in all operations.

## Phase 1: Setup & Infrastructure

Initialize the backend structure and install necessary dependencies for the database layer.

- [x] T001 Create backend directory structure: `/backend/src/models`, `/backend/src/database`, `/backend/src/repositories`
- [x] T002 Create backend requirements file with SQLModel dependencies in `/backend/requirements.txt`
- [x] T003 Create backend environment file `/backend/.env` for DATABASE_URL
- [x] T004 Create core config file `/backend/src/core/config.py` for database settings

## Phase 2: Foundation - Database Connection & Models

Establish the foundational database components before implementing business logic.

- [x] T005 Create database engine utility in `/backend/src/database/engine.py`
- [x] T006 Create database session utility in `/backend/src/database/session.py`
- [x] T007 Create base model in `/backend/src/database/base.py`
- [x] T008 [P] Create User model in `/backend/src/models/user.py`
- [x] T009 [P] Create Task model in `/backend/src/models/task.py` with user_id foreign key
- [x] T010 Create database initialization function to set up tables

## Phase 3: User Story 1 - Secure Task Storage [P1]

Implement the foundational ability to securely store tasks in the database with proper user isolation.

**Goal**: Enable users to store tasks in the database with secure user isolation.

**Independent Test Criteria**:
- System can store tasks associated with a verified user ID
- Only the owner can retrieve their tasks
- Data persists across application restarts

**Acceptance Tests**:
- [ ] T011 [US1] Write test verifying task creation with user_id
- [ ] T012 [US1] Write test verifying user A cannot access user B's tasks

**Implementation Tasks**:
- [x] T013 [US1] Create database initialization utility
- [x] T014 [US1] Implement create_task function in repository layer
- [x] T015 [US1] Implement get_tasks_for_user function with user_id filter
- [x] T016 [US1] Verify database connection works with Neon

## Phase 4: User Story 2 - Task CRUD Operations [P1]

Implement the complete set of CRUD operations for managing tasks.

**Goal**: Enable users to create, read, update, and delete their tasks with data integrity.

**Independent Test Criteria**:
- Users can perform all four operations on their own tasks
- User isolation is maintained during all operations
- Data integrity is preserved during updates

**Acceptance Tests**:
- [ ] T017 [US2] Write test for task update functionality
- [ ] T018 [US2] Write test for task deletion functionality
- [ ] T019 [US2] Write test ensuring update/delete operations only affect owner's tasks

**Implementation Tasks**:
- [x] T020 [US2] Implement get_task_by_id_for_user function
- [x] T021 [US2] Implement update_task_for_user function with user_id validation
- [x] T022 [US2] Implement delete_task_for_user function with user_id validation
- [x] T023 [US2] Add validation to ensure operations only affect owner's data

## Phase 5: User Story 3 - System Integration [P2]

Integrate the database layer with the authentication system to enable secure API operations.

**Goal**: Enable the database layer to work seamlessly with the authentication system using verified user IDs.

**Independent Test Criteria**:
- Database operations accept and utilize verified user ID parameter
- All queries automatically filter by authenticated user ID
- Authentication and database layers work together properly

**Acceptance Tests**:
- [ ] T024 [US3] Write integration test using mocked user_id
- [ ] T025 [US3] Write test verifying authenticated queries are properly filtered

**Implementation Tasks**:
- [x] T026 [US3] Create database session dependency in `/backend/src/dependencies.py`
- [x] T027 [US3] Create test endpoint `/api/db-test` to validate integration
- [x] T028 [US3] Implement helper functions to validate user ownership of tasks

## Phase 6: Validation & Security

Validate that all security requirements are met and the system is ready for handoff.

- [x] T029 Validate that all queries properly filter by user_id
- [x] T030 Test edge cases like invalid user_id access attempts
- [x] T031 Verify no data leakage between users
- [x] T032 Update CLAUDE.md to reflect operational secure data layer
- [x] T033 Document database layer for handoff to backend API development

## Dependencies

- T005-T010 must complete before T013-T015 (Foundation before US1)
- T008-T009 must complete before T014-T022 (Models before repository functions)
- T013-T015 must complete before T020-T022 (Basic CRUD before advanced operations)
- Authentication layer (P2-SPEC-1) must be available before T026-T027 (dependency on auth system)

## Parallel Execution Opportunities

- T008 and T009 can run in parallel (User and Task models)
- T005, T006, and T007 can run in parallel (Database utilities)
- T011 and T012 can run in parallel (US1 tests)
- T017, T018, and T019 can run in parallel (US2 tests)
- T024 and T025 can run in parallel (US3 tests)
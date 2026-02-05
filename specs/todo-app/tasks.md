---
description: "Task list for Todo In-Memory Python Console App implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below adjusted for todo app structure per plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan: src/, models/, utils/
- [X] T002 [P] Create src/todo_app.py main application file
- [X] T003 [P] Create src/models/ directory
- [X] T004 [P] Create src/utils/ directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create task data model in src/models/task.py
- [X] T006 [P] Create task management utilities in src/utils/cli_helpers.py
- [X] T007 Initialize in-memory task storage (tasks list and next_id counter)
- [X] T008 Create main menu structure in src/todo_app.py
- [X] T009 Set up basic CLI input validation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with title and description, assign unique ID, mark as incomplete by default

**Independent Test**: Add a task via CLI menu and verify it appears in the task list

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests first, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Contract test for add_task function in contracts/api-contract.md
- [X] T011 [P] [US1] Manual test for adding task with title and description

### Implementation for User Story 1

- [X] T012 [US1] Implement add_task function in src/models/task.py (depends on T005)
- [X] T013 [US1] Add add task menu option to main menu in src/todo_app.py (depends on T008)
- [X] T014 [US1] Create add task CLI interface in src/utils/cli_helpers.py (depends on T006)
- [X] T015 [US1] Add input validation for task creation in src/utils/cli_helpers.py (depends on T009)
- [X] T016 [US1] Implement auto-incrementing ID assignment (depends on T007)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Display all tasks with ID, title, and completion status in a user-friendly format

**Independent Test**: Add multiple tasks, then view the list to verify all tasks display correctly with their status

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T017 [P] [US2] Contract test for get_all_tasks function in contracts/api-contract.md
- [X] T018 [P] [US2] Manual test for viewing task list with mixed completion statuses

### Implementation for User Story 2

- [X] T019 [US2] Implement get_all_tasks function in src/models/task.py
- [X] T020 [US2] Add view tasks menu option to main menu in src/todo_app.py
- [X] T021 [US2] Create view tasks CLI interface in src/utils/cli_helpers.py
- [X] T022 [US2] Implement formatted display for task list with status indicators
- [X] T023 [US2] Handle empty task list scenario

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P3)

**Goal**: Toggle completion status of a task based on user input of task ID

**Independent Test**: Add a task, mark it as complete, verify status changed, then mark as incomplete again

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T024 [P] [US3] Contract test for toggle_task_completion function in contracts/api-contract.md
- [X] T025 [P] [US3] Manual test for toggling task completion status

### Implementation for User Story 3

- [X] T026 [US3] Implement toggle_task_completion function in src/models/task.py
- [X] T027 [US3] Add mark task menu option to main menu in src/todo_app.py
- [X] T028 [US3] Create mark task CLI interface in src/utils/cli_helpers.py
- [X] T029 [US3] Add validation to ensure task ID exists before toggling

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Allow users to modify task title and/or description by task ID

**Independent Test**: Add a task, update its title and description, verify changes persist

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US4] Contract test for update_task function in contracts/api-contract.md
- [X] T031 [P] [US4] Manual test for updating task title and description

### Implementation for User Story 4

- [X] T032 [US4] Implement update_task function in src/models/task.py
- [X] T033 [US4] Add update task menu option to main menu in src/todo_app.py
- [X] T034 [US4] Create update task CLI interface in src/utils/cli_helpers.py
- [X] T035 [US4] Add partial update capability (allow updating just title or just description)

**Checkpoint**: User stories 1, 2, 3, and 4 should now be independently functional

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Remove tasks by ID with validation to ensure ID exists before deletion

**Independent Test**: Add multiple tasks, delete one by ID, verify it's removed and others remain

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US5] Contract test for delete_task function in contracts/api-contract.md
- [X] T037 [P] [US5] Manual test for deleting tasks by ID

### Implementation for User Story 5

- [X] T038 [US5] Implement delete_task function in src/models/task.py
- [X] T039 [US5] Add delete task menu option to main menu in src/todo_app.py
- [X] T040 [US5] Create delete task CLI interface in src/utils/cli_helpers.py
- [X] T041 [US5] Add validation to ensure task ID exists before deletion
- [X] T042 [US5] Prevent ID reuse after deletion

**Checkpoint**: All five core user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Enhance error messages and user feedback throughout application
- [X] T044 [P] Improve CLI interface formatting and usability
- [X] T045 Add comprehensive input validation for all operations
- [X] T046 [P] Update README.md with setup and usage instructions
- [X] T047 [P] Add docstrings to all functions and classes
- [X] T048 Run quickstart.md validation to ensure all features work as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for add_task function in contracts/api-contract.md"
Task: "Manual test for adding task with title and description"

# Launch all models for User Story 1 together:
Task: "Implement add_task function in src/models/task.py"
Task: "Add input validation for task creation in src/utils/cli_helpers.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
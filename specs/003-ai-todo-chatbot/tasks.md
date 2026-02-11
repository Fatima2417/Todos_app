# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Configure environment variables (COHERE_API_KEY, NEXT_PUBLIC_OPENAI_DOMAIN_KEY) in .env
- [x] T002 Create backend/src/models/chat.py for SQLModel entity definitions
- [x] T003 [P] Create backend/src/api/mcp.py skeleton for MCP server
- [x] T004 [P] Create backend/src/services/agent.py skeleton for OpenAgentsSDK
- [x] T005 [P] Create backend/src/api/chat.py skeleton for chat endpoint

---

## Phase 2: Foundational

**Purpose**: Core infrastructure and data layer

- [x] T006 Implement Conversation and Message models in backend/src/models/chat.py
- [x] T007 [P] Create and run Alembic migration for chat tables
- [x] T008 [P] Implement JWT validation utility in backend/src/api/mcp.py
- [x] T009 [P] Initialize FastMCP server instance in backend/src/api/mcp.py
- [x] T010 [P] Configure Cohere client in backend/src/services/agent.py

---

## Phase 3: User Story 1 - Add Task via Natural Language (Priority: P1)

**Goal**: Enable users to add tasks using plain English commands.

**Independent Test**: Send "Add buy milk" via chat and verify task creation in the database.

- [x] T011 [US1] Implement add_task MCP tool in backend/src/api/mcp.py
- [x] T012 [US1] Implement core agent reasoning for task addition in backend/src/services/agent.py
- [x] T013 [US1] Implement POST /api/chat logic for User Story 1 in backend/src/api/chat.py
- [x] T014 [US1] Integrate OpenAI ChatKit widget in frontend/app/layout.tsx
- [x] T015 [US1] Connect ChatKit to /api/chat with JWT in frontend/app/layout.tsx

---

## Phase 4: User Story 2 - View and Manage Tasks via Chat (Priority: P2)

**Goal**: Enable users to list, complete, and delete tasks through the chat interface.

**Independent Test**: Ask "What are my tasks?" and verify the returned list.

- [x] T016 [US2] Implement list_tasks MCP tool in backend/src/api/mcp.py
- [x] T017 [US2] Implement update_task, complete_task, and delete_task MCP tools in backend/src/api/mcp.py
- [x] T018 [US2] Update agent service to support list/update/complete/delete intents in backend/src/services/agent.py
- [x] T019 [US2] Refine /api/chat endpoint to handle multiple tool results in backend/src/api/chat.py

---

## Phase 5: User Story 3 - Persistent Conversational History (Priority: P3)

**Goal**: Save and reload chat history for a seamless user experience.

**Independent Test**: Refresh page and verify old messages are still visible in the chat widget.

- [x] T020 [US3] Implement conversation history retrieval logic in backend/src/api/chat.py
- [x] T021 [US3] Implement message persistence logic (user/assistant) in backend/src/api/chat.py
- [x] T022 [US3] Update frontend to pass and maintain conversation_id in frontend/app/layout.tsx

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, error handling, and final validation.

- [x] T023 [P] Add global error handling middleware for chat in backend/src/api/chat.py
- [x] T024 [P] Implement user-friendly error responses for the AI agent in backend/src/services/agent.py
- [x] T025 [P] Final audit of JWT scoping in all MCP tools in backend/src/api/mcp.py
- [x] T026 [P] Run final integration tests in backend/tests/test_agent.py
- [x] T027 Run quickstart.md validation steps

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)**
2. **Foundational (Phase 2)** -> **User Story 1 (Phase 3)**
3. **User Story 1 (Phase 3)** -> **User Story 2 (Phase 4)** & **User Story 3 (Phase 5)**
4. **All User Stories** -> **Polish (Phase 6)**

### Parallel Opportunities
- Setup tasks (T001, T003-T005)
- Foundational tasks (T007-T010)
- Polish tasks marked [P]

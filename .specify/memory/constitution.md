<!--
Sync Impact Report:
- Version change: [TEMPLATE] -> 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] -> I. Spec-Driven Development (SDD)
    - [PRINCIPLE_2_NAME] -> II. Tool-First Intelligence (MCP)
    - [PRINCIPLE_3_NAME] -> III. Strict Security & Multi-tenancy
    - [PRINCIPLE_4_NAME] -> IV. Model-Driven Architecture (SQLModel)
    - [PRINCIPLE_5_NAME] -> V. Conversational Integrity
    - [PRINCIPLE_6_NAME] -> VI. Test-First & Verifiable Quality
- Added sections: Tech Stack Standards, Architectural Flow
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ aligned)
    - .specify/templates/spec-template.md (✅ aligned)
    - .specify/templates/tasks-template.md (✅ aligned)
- Follow-up TODOs: None.
-->

# Full-Stack AI Todo Application Constitution

## Core Principles

### I. Spec-Driven Development (SDD)
All functional changes MUST originate from a formal specification in the `/specs/` directory, followed by a technical implementation plan and a granular task list. Code implementation only begins after the specification and plan are ratified. This ensures architectural alignment and prevents scope creep.

### II. Tool-First Intelligence (MCP)
Every core business capability (CRUD operations, status transitions, etc.) MUST be exposed via standardized Model Context Protocol (MCP) tools. The AI agent MUST NOT interact with the database or business logic directly; it MUST use these standardized interfaces to ensure observability, control, and protocol-level isolation.

### III. Strict Security & Multi-tenancy
Mandatory JWT verification via Better Auth is required for every request. All data access MUST be strictly isolated by `user_id` at both the database layer (SQLModel) and the MCP tool level. Proving data isolation through automated security tests is a non-negotiable success criterion for every feature.

### IV. Model-Driven Architecture (SQLModel)
SQLModel serves as the single source of truth for database schema, API validation, and internal data structures. Every core entity (Task, Conversation, Message) MUST be defined as a SQLModel class to ensure type safety and consistency across the stack.

### V. Conversational Integrity
Every chat interaction MUST be persisted in the `Conversation` and `Message` tables. The chat endpoint MUST remain stateless, reconstructing the necessary context from the database for each agent invocation. This ensures that the system remains robust, auditable, and capable of long-term memory.

### VI. Test-First & Verifiable Quality
Test-Driven Development (TDD) is the standard for all core logic. Every User Story defined in a specification MUST have an associated independent test journey. No PR shall be merged without passing all unit, integration, and security-focused regression tests.

## Tech Stack Standards

The project strictly adheres to the following technology stack:
- **Backend**: FastAPI (Python 3.13+)
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Frontend**: Next.js 14+ with Tailwind CSS and OpenAI ChatKit
- **Authentication**: Better Auth with JWT
- **Intelligence**: OpenAgentsSDK for agent orchestration and MCP for tool definitions

## Architectural Flow

System interactions MUST follow this standard data flow:
1. **Request**: User message sent via OpenAI ChatKit with a JWT.
2. **Endpoint**: FastAPI validates the JWT and retrieves conversation history from the database.
3. **Reasoning**: OpenAgentsSDK Agent processes the prompt using history, the new message, and available MCP tools.
4. **Execution**: The Agent executes tool calls via the MCP Server, which performs database operations via SQLModel.
5. **Persistence**: The Agent response and user message are saved to the database.
6. **Delivery**: The natural language response is returned to the frontend.

## Governance

- **Supremacy**: This Constitution supersedes all other project documentation and practices.
- **Amendments**: Changes to these principles require a version bump (SemVer) and a corresponding update to the Sync Impact Report at the top of this file.
- **Compliance**: All Pull Requests MUST include a "Constitution Check" in their implementation plan to justify any deviations or confirm adherence to these rules.
- **Versioning**: MAJOR bumps for principle removals, MINOR for additions, PATCH for clarifications.

**Version**: 1.0.0 | **Ratified**: 2026-02-11 | **Last Amended**: 2026-02-11
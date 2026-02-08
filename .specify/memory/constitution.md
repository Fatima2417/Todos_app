<!-- SYNC IMPACT REPORT
Version change: 1.0.0 -> 2.0.0
Modified principles: Spec-Driven Development (SDD) First, Clean & Structured Python, Memory-Based Storage → Agentic Specialization, Full-Stack Architecture, Database Persistence
Added sections: Security by Default, Clean Architecture, Tech Stack Compliance, JWT Everywhere, User Data Isolation
Removed sections: Memory-Based Storage, Command-Line Interface Only, Platform Standardization
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending review
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development (SDD) First
All code must originate from Claude Code based on Markdown specs. No manual coding allowed. This ensures traceability, reduces defects, and maintains alignment between requirements and implementation. All work begins in `/specs/`.

### Agentic Specialization
The four specialized agents (`jwt-auth-specialist`, `neon-database-operator`, `fastapi-backend-architect`, `nextjs-frontend-engineer`) are the sole executors for their domains. All implementation tasks must be directed to the correct specialized agent based on the domain of work.

### Full-Stack Architecture
Build a complete web application with Next.js frontend, FastAPI backend, and Neon PostgreSQL database. Maintain clear separation between UI, API/Logic, and Persistence layers. Each layer must have defined interfaces and minimal coupling.

### Security by Default
All user data must be isolated at the database and API level. JWT tokens must authenticate all communication between frontend and backend. Security considerations must be addressed from the initial design phase, not added later.

### Clean Architecture
Maintain a strict separation of concerns: Frontend (UI), Backend (API/Logic), Database (Persistence), Auth (Security). Each layer has well-defined responsibilities and interfaces, promoting maintainability and testability.

### Tech Stack Compliance
Use only the technologies mandated in the hackathon brief (Next.js 16+ App Router, FastAPI, SQLModel, Neon PostgreSQL, Better Auth). Adhere to the specified versions and integration patterns to ensure compatibility and deployment readiness.

### API Contract First
Design all backend APIs with Pydantic models first, ensuring type-safe requests and responses. Frontend and backend contracts must be clearly defined before implementation to prevent integration issues.

## Additional Constraints

**No Manual Coding**: All implementation must be performed by Claude Code, guided by specs and executed by the designated agents. Manual code edits are prohibited.

**Phase II Scope**: Implement only the five Basic Level features (Add, Delete, Update, View, Mark Complete) within the full-stack architecture. Do not build Intermediate or Advanced features (e.g., priorities, due dates).

**Stateless Backend**: The FastAPI service must remain stateless. User session data must be stored in the JWT token or the database, not in server memory.

**Monorepo Structure**: The project must adhere to the Spec-Kit monorepo structure with a clear `/specs/` directory and organized frontend/backend/database sections.

**Environment Variables**: All secrets (Database URL, JWT Secret) and configuration must be managed via environment variables. Hardcoded credentials are prohibited.

## Development Workflow

**Specification Requirement**: Each feature requires a Markdown spec in `/specs/`. No implementation without a corresponding spec document. Specifications must include acceptance criteria and security requirements.

**Agentic Workflow Protocol**: All development cycles are initiated by the Project Orchestrator. For each task, specify which agent is responsible, provide context from the relevant spec, and deliver a precise implementation prompt.

**Integration Testing**: The system must demonstrate full-stack functionality with secure authentication, data persistence, and user isolation working end-to-end. All five Basic Level features must work for logged-in users.

## Governance

This constitution supersedes all other development practices. All code contributions must comply with these principles. Amendments require formal documentation and team approval. All pull requests and reviews must verify constitution compliance. This document serves as the definitive authority for development standards and practices.

**Version**: 2.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
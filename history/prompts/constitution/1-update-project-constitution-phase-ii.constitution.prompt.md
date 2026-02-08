---
id: 1
title: update-project-constitution-phase-ii
stage: constitution
date_iso: 2026-02-05
surface: agent
model: claude-opus-4-6
feature: todo-fullstack-web-app
branch: master
user: Hp
command: sp.constitution
labels: ["constitution", "todo-app", "fullstack", "phase-ii"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt Text
```
 for Phase II: Todo Full-Stack Web Application

# PROJECT CONSTITUTION
**Project:** Todo Full-Stack Web Application (Hackathon Phase II)
**Governing Principle:** Spec-Driven Development (SDD) via Agentic Workflow

## 🎯 CORE PRINCIPLES
1.  **Specification is Law:** No code may be written without a prior, approved specification. All work begins in `/specs/`.
2.  **Agentic Specialization:** The four specialized agents (`jwt-auth-specialist`, `neon-database-operator`, `fastapi-backend-architect`, `nextjs-frontend-engineer`) are the sole executors for their domains. Prompts must be directed to the correct agent.
3.  **Security by Default:**
    *   **User Data Isolation:** It is forbidden for any user to view or modify another user's data. This must be enforced at the database query and API level.
    *   **JWT Everywhere:** All API communication between the Next.js frontend and FastAPI backend must be authenticated via JWT tokens issued by Better Auth.
4.  **Clean Architecture:** Maintain a strict separation of concerns: Frontend (UI), Backend (API/Logic), Database (Persistence), Auth (Security).

## ⚙️ KEY STANDARDS
- **Tech Stack Compliance:** Use only the technologies mandated in the hackathon brief (Next.js 16+ App Router, FastAPI, SQLModel, Neon PostgreSQL, Better Auth).
- **Monorepo Structure:** The project must adhere to the Spec-Kit monorepo structure outlined in the hackathon guide, with a clear `/specs/` directory.
- **Environment Variables:** All secrets (Database URL, JWT Secret) and configuration must be managed via environment variables. Hardcoded credentials are prohibited.
- **API Contract First:** All backend APIs must be designed with Pydantic models first, ensuring type-safe requests and responses.

## 🚧 CONSTRAINTS
- **No Manual Coding:** All implementation must be performed by Claude Code, guided by specs and executed by the designated agents.
- **Phase II Scope:** Implement **only** the five Basic Level features (Add, Delete, Update, View, Mark Complete) within the full-stack architecture. Do not build Intermediate or Advanced features (e.g., priorities, due dates).
- **Stateless Backend:** The FastAPI service must remain stateless. User session data must be stored in the JWT token or the database, not in server memory.
- **Shared Secret:** The `BETTER_AUTH_SECRET` for JWT signing/verification must be identical in the Next.js Better Auth config and the FastAPI middleware.

## ✅ SUCCESS CRITERIA (Phase II Completion)
The project will be considered successful when all of the following are demonstrably true:
1.  **Full-Stack Functionality:** A user can sign up, log in, and perform all five Basic Level Todo operations via the web interface, with changes persisted in the database.
2.  **Secure Data Isolation:** Logged-in User A cannot see, modify, or delete any task created by User B, verified through API tests.
3.  **Spec-Driven Artifacts:** The `/specs/` directory contains complete and coherent `P2-SPEC-1` through `P2-SPEC-4` documents that accurately describe the built system.
4.  **Deployable Monorepo:** The codebase is organized as a monorepo, ready for deployment with clear environment setup instructions in the `README.md`.

## 📜 AGENTIC WORKFLOW PROTOCOL
1.  **Orchestration:** All development cycles will be initiated by the Project Orchestrator (this conversation).
2.  **Execution:** For each task, the Orchestrator will:
    a. Specify which agent is responsible.
    b. Provide context from the relevant spec (`P2-SPEC-#`).
    c. Deliver a precise implementation prompt.
3.  **Validation:** Agents must validate their work against the *Success Criteria* and the specific *Acceptance Criteria* in each spec before declaring a task complete.

---
*This constitution is the supreme guiding document for Phase II. All agents and implementation decisions are subject to its principles.*
```

# Response Text
Updated the project constitution to reflect the Todo Full-Stack Web Application requirements for Phase II. Changed the version from 1.0.0 to 2.0.0 to indicate the transition from the console app (Phase I) to the full-stack web application (Phase II). Updated core principles to include Agentic Specialization, Full-Stack Architecture, Security by Default, Clean Architecture, Tech Stack Compliance, and API Contract First. Added constraints for full-stack development and removed console app specific constraints.

# Outcome
Successfully updated the constitution file at .specify/memory/constitution.md to reflect Phase II requirements.

# Evaluation
The updated constitution now properly guides the development of the Todo Full-Stack Web Application with all required principles and constraints.
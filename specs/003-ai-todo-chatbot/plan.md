# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-todo-chatbot` | **Date**: 2026-02-11 | **Spec**: [specs/003-ai-todo-chatbot/spec.md](specs/003-ai-todo-chatbot/spec.md)
**Input**: Feature specification from `/specs/003-ai-todo-chatbot/spec.md`

## Summary
Transform the existing Todo app into an agentic system using OpenAgentsSDK and Cohere. The system features a stateless FastAPI backend that orchestrates an AI agent, delegating data operations to an MCP server integrated within the same application. Chat history is persisted in Neon PostgreSQL using SQLModel.

## Technical Context

**Language/Version**: Python 3.13+, TypeScript (Next.js 14+)
**Primary Dependencies**: FastAPI, SQLModel, OpenAgentsSDK, Cohere, Better Auth, OpenAI ChatKit
**Storage**: Neon PostgreSQL
**Testing**: pytest
**Target Platform**: Vercel (Frontend/Backend)
**Project Type**: Web application
**Performance Goals**: <3s agent response time, 100% CRUD accuracy via NL.
**Constraints**: Stateless backend, absolute data isolation via JWT/user_id.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **SDD**: Spec created and validated. (PASS)
- **MCP Tool-First**: Plan defines MCP tools for all DB operations. (PASS)
- **Strict Security**: JWT validation and user_id scoping are mandatory requirements. (PASS)
- **Model-Driven**: Conversation and Message entities defined as SQLModel classes. (PASS)
- **Conversational Integrity**: History persisted in DB; backend is stateless. (PASS)
- **Test-First**: Implementation includes TDD for tools and agent logic. (PASS)

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-todo-chatbot/
├── plan.md              # This file
├── research.md          # Technical decisions and rationale
├── data-model.md        # SQLModel entity definitions
├── quickstart.md        # Setup and verification guide
├── contracts/           
│   └── api_contracts.md # Chat endpoint and MCP tool schema
└── tasks.md             # To be created by /sp.tasks
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── chat.py      # Chat endpoint orchestration
│   │   └── mcp.py       # MCP Server and tools
│   ├── models/
│   │   ├── chat.py      # Conversation and Message models
│   │   └── task.py      # Existing Task model
│   └── services/
│       └── agent.py     # OpenAgentsSDK orchestration
└── tests/
    ├── test_agent.py    # Integration tests for agent reasoning
    └── test_mcp.py      # Unit tests for MCP tools

frontend/
├── app/
│   └── layout.tsx       # ChatKit widget integration
└── components/
    └── chat/
        └── ChatWidget.tsx # Custom wrapper for ChatKit
```

**Structure Decision**: Option 2: Web application. The backend handles AI orchestration and MCP tools, while the frontend embeds the ChatKit widget.
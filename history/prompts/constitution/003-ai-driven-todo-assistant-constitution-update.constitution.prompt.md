---
id: 3
title: AI-Driven Todo Assistant Constitution Update
stage: constitution
date: 2026-02-11
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: Hp
command: sp.constitution
labels: ["constitution", "mcp", "fastapi", "sqlmodel", "better-auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Tool Protocol: Official MCP SDK to build a server exposing Todo operations (add_task, list_tasks, etc.) as standardized tools for the agent.

Backend Framework: FastAPI to serve the chat endpoint (POST /api/{user_id}/chat) and host the MCP server.

Data Layer: SQLModel with Neon PostgreSQL. Must extend existing Task model with new Conversation and Message models.

Authentication: Better Auth with JWT. The chat endpoint and all MCP tools must validate the user's JWT token and strictly enforce data isolation.

Frontend Interface: OpenAI ChatKit for the user-facing chat UI, configured with your domain key.

Section 3: Core Architecture & Workflow
The system must follow this defined data flow and structure:

graph LR
    A[User Message via ChatKit] --> B[FastAPI Chat Endpoint]
    B --> C{Agent via OpenAgentsSDK}
    C --> D[MCP Server Tools]
    D --> E[(Neon Database)]
    E --> D
    D --> C
    C --> F[Agent Response]
    F --> B
    B --> A
Workflow Rules:

The chat endpoint receives a user message and a valid JWT.

It fetches the recent conversation history from the Message table in the database.

It calls the OpenAgentsSDK Agent, passing the history, new message, and available MCP tools.

The Agent reasons about the request and decides which tool(s) to call.

The Agent executes tool calls to the MCP Server. Each tool function contains the business logic (via SQLModel) to interact with the database.

The Agent formulates a natural language response based on the tool results.

The endpoint saves both the user message and agent's response to the database.

The agent's response is returned to the ChatKit frontend.

Section 4: Quality & Validation Standards
Code Quality: All AI-generated code must adhere to PEP 8 (Python) and common React/TypeScript conventions. It must include error handling for common failure cases (e.g., task not found, database errors).

Agent Behavior: The Agent must confirm actions (e.g., "I've added 'Buy groceries' to your list.") and handle ambiguous commands gracefully (e.g., "Which task do you want to delete?").

Security: JWT verification is mandatory. Absolute user data isolation must be proven—no user can access or modify another user's tasks via any endpoint.

Documentation: The /specs/ folder must contain comprehensive spec files for:

agent_behavior.md: Defines how the agent should interpret common phrases.

mcp_tools.md: Detailed specification for each tool (parameters, returns, examples).

database_schema.md: Updated schema for Conversation and Message tables.

api_endpoints.md: Specification for the chat endpoint.

Section 5: Implementation Guide for Your Stack
Set Up Cohere & OpenAgentsSDK: Initialize the OpenAgentsSDK agent with the Cohere client. Your core prompt should instruct it to act as a helpful Todo assistant that uses the provided MCP tools.

Build the MCP Server: Use the Official MCP SDK to create a server where each tool (e.g., add_task) is a function that accepts the validated user_id and task parameters, performs the database operation via SQLModel, and returns a clear result.

Integrate Stateless Chat Endpoint: The FastAPI chat endpoint should authenticate the user, manage conversation history in the database, orchestrate the Agent, and be instantly ready for the next request.

Connect the Frontend: Configure the OpenAI ChatKit component to point to your backend chat endpoint, ensuring it passes the user's JWT token.

## Response snapshot

Created concrete constitution v1.0.0 with concrete principles for MCP Tool usage, FastAPI architecture, SQLModel data management, and Better Auth security. Defined the core architectural flow and quality standards as project-wide non-negotiable rules.

## Outcome

- ✅ Impact: Established core architecture and security principles for the AI-driven Todo system.
- 🧪 Tests: N/A (Documentation change)
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Run /sp.specify to build the feature specifications for agent behavior, MCP tools, database schema, and API endpoints.
- 🧠 Reflection: Successfully integrated specific user technical requirements into the project's governance document, providing a solid foundation for Spec-Driven Development.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null

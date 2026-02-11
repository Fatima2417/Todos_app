# Research: AI-Powered Todo Chatbot

## Decision 1: OpenAgentsSDK & Cohere Integration
- **Decision**: Use `OpenAgentsSDK` to orchestrate the AI agent with the `Cohere` client.
- **Rationale**: The SDK provides a structured way to define agents and connect them to MCP tools. Cohere offers robust natural language understanding for task extraction.
- **Alternatives Considered**: Direct Cohere API calls (rejected as it requires manual tool-calling logic implementation).

## Decision 2: MCP Server Implementation
- **Decision**: Integrate the MCP server directly as a router within the existing FastAPI backend.
- **Rationale**: Simplifies deployment and allows sharing the same SQLModel database session and authentication middleware.
- **Alternatives Considered**: Standalone microservice (rejected due to increased complexity and overhead for this scope).

## Decision 3: Conversation History Management
- **Decision**: Fetch the last 10 messages from the `Message` table for each request to provide context to the agent.
- **Rationale**: Provides sufficient context for most task-related conversations while keeping token usage within reasonable limits.
- **Alternatives Considered**: Passing full history (risk of token overflow), Summarization (complex to implement).

## Decision 4: Frontend Chat UI
- **Decision**: Embed `OpenAI ChatKit` as a widget in the Next.js layout.
- **Rationale**: Provides a professional, ready-to-use conversational UI that can be easily connected to our custom backend endpoint.
- **Alternatives Considered**: Custom React chat UI (rejected as it would take significant development time away from core logic).

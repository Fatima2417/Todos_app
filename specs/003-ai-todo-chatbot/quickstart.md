# Quickstart: AI-Powered Todo Chatbot

## Implementation Steps

1. **Database Update**: Run migrations to create `Conversation` and `Message` tables.
2. **MCP Server**: Implement the MCP Router in `backend/src/api/mcp.py` with the 5 core tools.
3. **Agent Logic**: Implement the OpenAgentsSDK orchestration in `backend/src/services/agent.py`.
4. **Chat Endpoint**: Create the `POST /api/chat` route in `backend/src/api/chat.py`.
5. **Frontend Widget**: Integrate `OpenAI ChatKit` in `frontend/app/layout.tsx` or as a standalone component.
6. **Authentication**: Ensure JWT tokens are passed from the frontend and validated in the backend.

## Verification

### Automated Tests
```bash
# Run backend tests
pytest backend/tests/test_agent.py
pytest backend/tests/test_mcp_tools.py
```

### Manual Verification
1. Login to the web application.
2. Open the chat widget.
3. Type: "Show my tasks".
4. Type: "Add a task to test the chatbot".
5. Verify the task appears in the main list.
6. Type: "Complete the task I just added".
7. Verify the task is marked as done.

# Data Model: AI-Powered Todo Chatbot

## Entities

### Conversation
- **id**: UUID (Primary Key)
- **user_id**: String (Foreign Key to User, used for data isolation)
- **created_at**: DateTime
- **updated_at**: DateTime

### Message
- **id**: UUID (Primary Key)
- **conversation_id**: UUID (Foreign Key to Conversation)
- **role**: String (Enum: "user", "assistant")
- **content**: Text (The message text)
- **created_at**: DateTime

### Task (Extended)
- *Existing attributes preserved*: id, user_id, title, is_completed
- *Interaction*: Managed via MCP Tools called by the AI Agent.

## Relationships
- **User** has many **Conversations**.
- **Conversation** has many **Messages**.
- **User** has many **Tasks**.

## Validation Rules
- `user_id` MUST be present and validated against the JWT for every database operation.
- `role` MUST be either "user" or "assistant".
- `content` MUST NOT be empty.

import os
import cohere
from typing import List, Dict

# T010: Configure Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Check if we are in mock mode (placeholder key)
IS_MOCK = not COHERE_API_KEY or COHERE_API_KEY == "your_cohere_api_key_here"

# Initialize Cohere client if not in mock mode
co = None
if not IS_MOCK:
    try:
        co = cohere.Client(api_key=COHERE_API_KEY)
    except Exception as e:
        print(f"Failed to initialize Cohere client: {e}")
        IS_MOCK = True

def run_todo_agent(message: str, history: List[Dict[str, str]], jwt_token: str):
    """
    Orchestrates the agent reasoning. 
    Returns mock responses if COHERE_API_KEY is not configured.
    """
    
    if IS_MOCK:
        # T012: Implementation logic for User Story 1 (Mock)
        msg_lower = message.lower()
        if "add" in msg_lower:
            # Simulate add_task tool call
            from ..api.mcp import add_task
            # Simple heuristic to extract title
            title = message.replace("add", "").replace("task", "").strip()
            if not title: title = "New Task"
            result = add_task(jwt_token=jwt_token, title=title)
            return f"I've added that for you. {result}", "mock_conv_123", [{"name": "add_task", "parameters": {"title": title}}]
        elif "list" in msg_lower or "show" in msg_lower:
            from ..api.mcp import list_tasks
            result = list_tasks(jwt_token=jwt_token)
            return f"Here are your tasks:\n{result}", "mock_conv_123", [{"name": "list_tasks", "parameters": {}}]
        elif "complete" in msg_lower or "done" in msg_lower:
            from ..api.mcp import complete_task
            # Try to extract ID
            import re
            match = re.search(r'\d+', msg_lower)
            if match:
                result = complete_task(jwt_token=jwt_token, task_id=int(match.group()))
                return f"Updated! {result}", "mock_conv_123", [{"name": "complete_task", "parameters": {"task_id": int(match.group())}}]
            return "Which task ID should I mark as complete?", "mock_conv_123", []
        elif "delete" in msg_lower:
            from ..api.mcp import delete_task
            import re
            match = re.search(r'\d+', msg_lower)
            if match:
                result = delete_task(jwt_token=jwt_token, task_id=int(match.group()))
                return f"Deleted! {result}", "mock_conv_123", [{"name": "delete_task", "parameters": {"task_id": int(match.group())}}]
            return "Which task ID should I delete?", "mock_conv_123", []
        
        return "Hi! I'm your Todo Assistant (Mock Mode). You can ask me to add, list, complete, or delete tasks.", "mock_conv_123", []

    # REAL AGENT LOGIC (Cohere)
    # Define the tools for Cohere
    tools = [
        {
            "name": "add_task",
            "description": "Adds a new task to the user's todo list.",
            "parameter_definitions": {
                "title": {
                    "description": "The title of the task to add.",
                    "type": "string",
                    "required": True
                }
            }
        },
        {
            "name": "list_tasks",
            "description": "Lists all pending tasks for the user.",
            "parameter_definitions": {}
        },
        {
            "name": "update_task",
            "description": "Updates the title of an existing task.",
            "parameter_definitions": {
                "task_id": {
                    "description": "The ID of the task to update.",
                    "type": "integer",
                    "required": True
                },
                "title": {
                    "description": "The new title for the task.",
                    "type": "string",
                    "required": True
                }
            }
        },
        {
            "name": "complete_task",
            "description": "Marks a task as completed.",
            "parameter_definitions": {
                "task_id": {
                    "description": "The ID of the task to complete.",
                    "type": "integer",
                    "required": True
                }
            }
        },
        {
            "name": "delete_task",
            "description": "Deletes a task from the list.",
            "parameter_definitions": {
                "task_id": {
                    "description": "The ID of the task to delete.",
                    "type": "integer",
                    "required": True
                }
            }
        }
    ]
    
    preamble = """
    You are a helpful Todo assistant. 
    You help users manage their tasks using the provided MCP tools.
    Always verify actions with the user and be concise.
    When asked to list tasks, use the list_tasks tool.
    When asked to complete or delete a task, use the task_id provided by the user or found in the history.
    """
    
    try:
        response = co.chat(
            message=message,
            chat_history=history,
            tools=tools,
            preamble=preamble
        )
        
        conv_id = getattr(response, 'conversation_id', 'no_conv_id')
        
        if response.tool_calls:
            from ..api.mcp import add_task, list_tasks, update_task, complete_task, delete_task
            
            tool_results = []
            serialized_tool_calls = []
            for tool_call in response.tool_calls:
                # Store serialized tool call for database
                serialized_tool_calls.append({
                    "name": tool_call.name,
                    "parameters": tool_call.parameters
                })
                
                result = None
                print(f"Agent wants to call tool: {tool_call.name} with params: {tool_call.parameters}")
                try:
                    if tool_call.name == "add_task":
                        result = add_task(jwt_token=jwt_token, title=tool_call.parameters.get("title"))
                    elif tool_call.name == "list_tasks":
                        result = list_tasks(jwt_token=jwt_token)
                    elif tool_call.name == "update_task":
                        result = update_task(jwt_token=jwt_token, task_id=tool_call.parameters.get("task_id"), title=tool_call.parameters.get("title"))
                    elif tool_call.name == "complete_task":
                        result = complete_task(jwt_token=jwt_token, task_id=tool_call.parameters.get("task_id"))
                    elif tool_call.name == "delete_task":
                        result = delete_task(jwt_token=jwt_token, task_id=tool_call.parameters.get("task_id"))
                except Exception as e:
                    print(f"Error executing tool {tool_call.name}: {e}")
                    result = f"Error executing {tool_call.name}: {str(e)}"
                
                if result:
                    print(f"Tool {tool_call.name} result: {result}")
                    tool_results.append({
                        "call": tool_call,
                        "outputs": [{"result": result}]
                    })
            
            # Get final response with tool results
            final_response = co.chat(
                chat_history=history,
                message=message,
                tool_results=tool_results,
                preamble=preamble,
                force_single_step=True
            )
            return final_response.text, conv_id, serialized_tool_calls
        
        return response.text, conv_id, []
    except Exception as e:
        print(f"Cohere API error: {e}")
        return f"I'm sorry, I encountered an error with the AI service: {e}", "error_conv", []

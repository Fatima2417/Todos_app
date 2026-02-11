from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from ..dependencies import get_current_user
from ..services.agent import run_todo_agent
from ..database.engine import engine
from ..models.chat import Conversation, Message
from sqlmodel import Session, select
import uuid

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: Optional[List[dict]] = None

@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    chat_req: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        jwt_token = auth_header.split(" ")[1]
    except (IndexError, AttributeError):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    with Session(engine) as session:
        try:
            # T020: Find or create conversation (US3 partial)
            if chat_req.conversation_id:
                try:
                    db_conv = session.get(Conversation, uuid.UUID(chat_req.conversation_id))
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid conversation_id format")
                
                if not db_conv or db_conv.user_id != user_id:
                    # Security: User can only access their own conversations
                    db_conv = Conversation(user_id=user_id)
                    session.add(db_conv)
                    session.commit()
                    session.refresh(db_conv)
            else:
                db_conv = Conversation(user_id=user_id)
                session.add(db_conv)
                session.commit()
                session.refresh(db_conv)
                
            # Fetch history (last 10 messages)
            statement = select(Message).where(Message.conversation_id == db_conv.id).order_by(Message.created_at.desc()).limit(10)
            db_messages = session.exec(statement).all()
            history = [{"role": m.role.upper() if m.role == "user" else "CHATBOT", "message": m.content} for m in reversed(db_messages)]
            
            # T013: Logic for User Story 1
            try:
                agent_text, _, tool_calls = run_todo_agent(chat_req.message, history, jwt_token)
            except Exception as e:
                print(f"Agent error: {str(e)}")
                agent_text = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
                tool_calls = []
            
            # T021: Save messages (US3 partial)
            user_msg = Message(
                conversation_id=db_conv.id, 
                user_id=user_id,
                role="user", 
                content=chat_req.message
            )
            assistant_msg = Message(
                conversation_id=db_conv.id, 
                user_id=user_id,
                role="assistant", 
                content=agent_text,
                tool_calls=tool_calls
            )
            session.add(user_msg)
            session.add(assistant_msg)
            session.commit()
            
            return ChatResponse(
                response=agent_text, 
                conversation_id=str(db_conv.id),
                tool_calls=tool_calls
            )
        except Exception as e:
            session.rollback()
            print(f"Chat endpoint error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500, 
                detail=f"Internal Server Error: {str(e)}. Check backend logs for full traceback."
            )

from fastapi import APIRouter, HTTPException
from typing import List
from app.models import ChatMessage, ChatResponse
from app.services import ai_agent

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    """
    Chat with the AI agent for welcome kit assistance.
    
    The AI agent can help with:
    - Service plan information
    - Welcome kit ordering
    - SIM activation instructions
    - General support questions
    """
    try:
        response, session_id, suggestions = ai_agent.process_chat_message(
            message.message,
            message.session_id
        )
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.get("/health")
async def chat_health():
    """Check if the chat service is healthy."""
    return {"status": "healthy", "service": "chat"}

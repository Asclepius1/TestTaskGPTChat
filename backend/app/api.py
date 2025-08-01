from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatgpt import ask_chatgpt, AIRequestError

class Message(BaseModel):
    text: str

router = APIRouter()

@router.post("/chat")
async def chat(msg: Message):
    try:
        response = await ask_chatgpt(msg.text)
        return {"reply": response}
    
    except AIRequestError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while processing your request. {e}")
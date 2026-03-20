from fastapi import APIRouter
import httpx
from backend.schemas import ChatRequest, ChatResponse
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(tags=["Chat"])
AI_BASE= os.getenv("AI_SERVICE_URL", "http://localhost:8001")


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/chat/ask", json=req.model_dump())
        r.raise_for_status()
        return r.json()

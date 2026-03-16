from fastapi import APIRouter
import httpx
from backend.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["Chat"])
AI_BASE = "http://localhost:8001"


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/chat/ask", json=req.model_dump())
        r.raise_for_status()
        return r.json()

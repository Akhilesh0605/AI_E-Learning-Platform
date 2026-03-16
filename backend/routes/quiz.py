from fastapi import APIRouter
import httpx
from backend.schemas import QuizGenerateRequest, QuizEvaluateRequest

router = APIRouter(tags=["Quiz"])
AI_BASE = "http://localhost:8001"


@router.post("/quiz/generate")
async def generate_quiz(req: QuizGenerateRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/quiz/generate", json=req.model_dump())
        r.raise_for_status()
        return r.json()


@router.post("/quiz/evaluate")
async def evaluate_quiz(req: QuizEvaluateRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/quiz/evaluate", json=req.model_dump())
        r.raise_for_status()
        return r.json()

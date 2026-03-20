from fastapi import APIRouter
import httpx
from schemas import PredictQuestionsRequest
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(tags=["Questions"])
AI_BASE= os.getenv("AI_SERVICE_URL", "http://localhost:8001")


@router.post("/questions/predict")
async def predict_questions(req: PredictQuestionsRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/predict/important-questions", json=req.model_dump())
        r.raise_for_status()
        return r.json()

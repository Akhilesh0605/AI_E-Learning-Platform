from fastapi import APIRouter, UploadFile, File, Form
import httpx
from schemas import SummarizeRequest
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(tags=["Notes"])
AI_BASE= os.getenv("AI_SERVICE_URL", "http://localhost:8001")


@router.post("/notes/from-pdf")
async def notes_from_pdf(file: UploadFile = File(...), level: str = Form("beginner")):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"{AI_BASE}/ai/notes/from-pdf",
            files={"file": (file.filename, await file.read(), file.content_type)},
            data={"level": level},
        )
        r.raise_for_status()
        return r.json()


@router.post("/notes/summarize")
async def summarize(req: SummarizeRequest):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE}/ai/notes/summarize", json=req.model_dump())
        r.raise_for_status()
        return r.json()

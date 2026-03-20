from fastapi import APIRouter
import httpx
from backend.schemas import CourseGenerateRequest, ModuleContentRequest
import os

router = APIRouter(tags=["Course"])

AI_BASE= os.getenv("AI_SERVICE_URL", "http://localhost:8001")
@router.post("/course/generate")
async def generate_course(req: CourseGenerateRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{AI_BASE}/ai/course/generate", json=req.model_dump())
        r.raise_for_status()
        return r.json()


@router.post("/course/module-content")
async def module_content(req: ModuleContentRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{AI_BASE}/ai/course/module-content", json=req.model_dump())
        r.raise_for_status()
        return r.json()

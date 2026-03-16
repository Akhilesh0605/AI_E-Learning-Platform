from pydantic import BaseModel, Field
from typing import List, Optional


# ── Chat ──────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str
    subject: str = "general"
    level: str = "beginner"


class ChatResponse(BaseModel):
    answer: str
    subject: str
    level: str


# ── Quiz ──────────────────────────────────────────────────────────────────────
class QuizGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "easy"


class QuizEvaluateRequest(BaseModel):
    question: str
    correct_answer: str
    student_answer: str


# ── Notes ─────────────────────────────────────────────────────────────────────
class SummarizeRequest(BaseModel):
    text: str
    level: str = "beginner"


# ── Questions ─────────────────────────────────────────────────────────────────
class PredictQuestionsRequest(BaseModel):
    topic: str
    level: str = "beginner"
    exam_type: str = "university"


# ── Course ────────────────────────────────────────────────────────────────────
class CourseGenerateRequest(BaseModel):
    topic: str
    level: str = "beginner"
    num_modules: int = 5


class ModuleContentRequest(BaseModel):
    topic: str
    module_title: str
    level: str = "beginner"

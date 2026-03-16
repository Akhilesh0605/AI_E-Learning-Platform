from fastapi import APIRouter
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Teaching Agent"])

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

LEVEL_INSTRUCTIONS = {
    "beginner": (
        "You are a patient, encouraging teacher. Use simple language, real-world analogies, "
        "and short sentences. Define every technical term you use. Avoid all jargon. "
        "Imagine you are explaining to a 12-year-old who is curious but brand new to the topic."
    ),
    "intermediate": (
        "You are a knowledgeable instructor. Assume the student knows the fundamentals. "
        "Focus on the *how* and *why*. Use concrete code examples or worked examples. "
        "Introduce standard terminology naturally."
    ),
    "advanced": (
        "You are an expert peer. Assume a strong technical foundation. "
        "Dive into deep theory, internals, edge cases, tradeoffs, and production-level patterns. "
        "Reference relevant papers, design patterns, or architectural considerations where appropriate."
    ),
}


class TeachRequest(BaseModel):
    question: str
    subject: str = "general"
    level: str = "beginner"


class TeachResponse(BaseModel):
    answer: str
    subject: str
    level: str


@router.post("/chat/ask", response_model=TeachResponse)
async def ask(req: TeachRequest):
    level_hint = LEVEL_INSTRUCTIONS.get(req.level, LEVEL_INSTRUCTIONS["beginner"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"{level_hint}\n\nSubject area: {{subject}}.\n"
            "Provide a clear, well-structured explanation.",
        ),
        ("human", "{question}"),
    ])

    chain = prompt | llm
    result = chain.invoke({"subject": req.subject, "question": req.question})
    return TeachResponse(answer=result.content, subject=req.subject, level=req.level)

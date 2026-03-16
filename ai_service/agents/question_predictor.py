import json
import re
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Question Predictor"])

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.4)

EXAM_CONTEXT = {
    "university": (
        "These are university-level exam questions. Focus on conceptual understanding, "
        "derivations, comparisons, and application-based problems. "
        "Include long-answer and short-answer question types."
    ),
    "competitive": (
        "These are competitive exam questions (e.g., GATE, GRE, competitive coding). "
        "Focus on tricky MCQs, time-bound problem solving, and edge cases. "
        "Questions should be concise but cognitively demanding."
    ),
    "school": (
        "These are school-level exam questions. Keep them straightforward and curriculum-aligned. "
        "Mix definition, short-answer, and application questions at an age-appropriate level."
    ),
}

LEVEL_DEPTH = {
    "beginner": "basic recall, definitions, and simple applications",
    "intermediate": "conceptual understanding, worked examples, and moderate problem solving",
    "advanced": "deep analysis, system design, edge cases, and complex problem solving",
}

SCHEMA = """{{
  "topic": "string",
  "level": "string",
  "exam_type": "string",
  "predicted_questions": [
    {{
      "question_number": integer,
      "question": "string",
      "question_type": "MCQ|Short Answer|Long Answer|Problem",
      "reason_for_importance": "string",
      "marks_weightage": "string",
      "hint": "string"
    }}
  ],
  "high_priority_topics": ["string"],
  "study_tip": "string"
}}"""


class PredictRequest(BaseModel):
    topic: str
    level: str = "beginner"
    exam_type: str = "university"


def _extract_json(text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
    return json.loads(cleaned)


@router.post("/predict/important-questions")
async def predict_questions(req: PredictRequest):
    exam_hint = EXAM_CONTEXT.get(req.exam_type, EXAM_CONTEXT["university"])
    level_hint = LEVEL_DEPTH.get(req.level, LEVEL_DEPTH["beginner"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an experienced exam coach with deep knowledge of question patterns. "
            f"{exam_hint}\n"
            f"Target depth: {level_hint}.\n\n"
            "Predict the most likely important questions that will appear. "
            "For each question, explain WHY it is important and its typical marks weightage.\n\n"
            "Return ONLY valid JSON matching this schema — no prose, no markdown fences:\n"
            f"{SCHEMA}",
        ),
        (
            "human",
            "Predict important exam questions for topic: '{topic}', level: {level}, exam type: {exam_type}.",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({
        "topic": req.topic,
        "level": req.level,
        "exam_type": req.exam_type,
    })

    try:
        predictions = _extract_json(result.content)
    except json.JSONDecodeError:
        predictions = {"raw": result.content, "parse_error": "Could not parse JSON"}

    return predictions

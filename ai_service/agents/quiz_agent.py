import json
import re
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Quiz Agent"])

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.5)

DIFFICULTY_CONTEXT = {
    "easy": "basic recall and definition questions, suitable for beginners",
    "medium": "application and understanding questions, suitable for intermediate learners",
    "hard": "analysis, synthesis, and tricky edge-case questions, suitable for advanced learners",
}

QUIZ_SCHEMA = """{
  "topic": "string",
  "difficulty": "string",
  "questions": [
    {
      "question_number": integer,
      "question": "string",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A|B|C|D",
      "explanation": "string"
    }
  ]
}"""


class QuizGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "easy"


class QuizEvaluateRequest(BaseModel):
    question: str
    correct_answer: str
    student_answer: str


def _extract_json(text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
    return json.loads(cleaned)


@router.post("/quiz/generate")
async def generate_quiz(req: QuizGenerateRequest):
    diff_hint = DIFFICULTY_CONTEXT.get(req.difficulty, DIFFICULTY_CONTEXT["easy"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an expert quiz designer. Create {diff_hint}.\n\n"
            "Return ONLY valid JSON matching this schema — no prose, no markdown fences:\n"
            f"{QUIZ_SCHEMA}",
        ),
        (
            "human",
            "Generate {num_questions} multiple-choice questions on '{topic}' at {difficulty} difficulty.",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({
        "topic": req.topic,
        "num_questions": req.num_questions,
        "difficulty": req.difficulty,
    })

    try:
        quiz_data = _extract_json(result.content)
    except json.JSONDecodeError:
        quiz_data = {"raw": result.content, "parse_error": "Could not parse JSON"}

    return quiz_data


@router.post("/quiz/evaluate")
async def evaluate_quiz(req: QuizEvaluateRequest):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a fair and constructive quiz evaluator. "
            "Compare the student's answer to the correct answer. "
            "Be generous with partial credit for correct reasoning even if wording differs. "
            "Return JSON: {\"score\": 0-100, \"is_correct\": bool, \"feedback\": \"string\", "
            "\"key_points_missed\": [\"string\"]}. No markdown fences.",
        ),
        (
            "human",
            "Question: {question}\nCorrect Answer: {correct_answer}\nStudent Answer: {student_answer}",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({
        "question": req.question,
        "correct_answer": req.correct_answer,
        "student_answer": req.student_answer,
    })

    try:
        evaluation = _extract_json(result.content)
    except json.JSONDecodeError:
        evaluation = {"raw": result.content, "parse_error": "Could not parse JSON"}

    return evaluation

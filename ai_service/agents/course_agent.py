import json
import re
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Course Generator"])

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.4)

LEVEL_CONTEXT = {
    "beginner": (
        "Start from absolute scratch. Assume zero prior knowledge. "
        "Each module should build gently on the previous one. "
        "Difficulty scores range from 1 to 3. Use simple prerequisite concepts only."
    ),
    "intermediate": (
        "Assume the learner knows the basics. Focus on application, patterns, and real-world usage. "
        "Each module should deepen practical skill. Difficulty scores range from 4 to 6."
    ),
    "advanced": (
        "Assume strong foundational knowledge. Cover internals, optimization, system design, "
        "architectural tradeoffs, and production-grade patterns. "
        "Difficulty scores range from 7 to 10."
    ),
}

COURSE_SCHEMA = """{{
  "course_title": "string",
  "level": "string",
  "total_modules": integer,
  "modules": [
    {{
      "module_number": integer,
      "title": "string",
      "description": "string",
      "topics_covered": ["string"],
      "learning_outcomes": ["string"],
      "estimated_time": "string",
      "difficulty_score": integer
    }}
  ],
  "prerequisites": ["string"],
  "final_project_idea": "string"
}}"""

class CourseRequest(BaseModel):
    topic: str
    level: str = "beginner"
    num_modules: int = 5


class ModuleContentRequest(BaseModel):
    topic: str
    module_title: str
    level: str = "beginner"


def _extract_json(text: str) -> dict:
    """Strip markdown fences and parse JSON."""
    cleaned = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
    return json.loads(cleaned)


@router.post("/course/generate")
async def generate_course(req: CourseRequest):
    level_hint = LEVEL_CONTEXT.get(req.level, LEVEL_CONTEXT["beginner"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are an expert curriculum designer. {level_hint}\n\n"
            "Return ONLY valid JSON matching this schema — no prose, no markdown fences:\n"
            f"{COURSE_SCHEMA}",
        ),
        (
            "human",
            "Design a {num_modules}-module course on '{topic}' for {level} learners.",
        ),
    ])

    chain = prompt | llm
    result = chain.invoke({
        "topic": req.topic,
        "level": req.level,
        "num_modules": req.num_modules,
    })

    try:
        course_data = _extract_json(result.content)
    except json.JSONDecodeError:
        course_data = {"raw": result.content, "parse_error": "Could not parse JSON — raw output returned"}

    return course_data


MODULE_CONTENT_PROMPT = """You are a world-class instructor creating detailed module content.
Level: {level}

Level rules:
- beginner  → plain language, step-by-step, real-world analogies, define every term
- intermediate → assume basics known, explain the "why", include working examples
- advanced → deep internals, edge cases, tradeoffs, production patterns, benchmark notes

Topic: {topic}
Module: {module_title}

Return a JSON object with these keys:
{{
  "module_title": "string",
  "overview": "string",
  "key_concepts": ["string"],
  "detailed_explanation": "string (markdown supported)",
  "examples": ["string"],
  "code_snippets": ["string"],
  "mini_exercise": {{
    "description": "string",
    "hints": ["string"],
    "expected_outcome": "string"
  }},
  "further_reading": ["string"]
}}

Return ONLY valid JSON, no markdown fences."""


@router.post("/course/module-content")
async def module_content(req: ModuleContentRequest):
    prompt = ChatPromptTemplate.from_messages([
        ("system", MODULE_CONTENT_PROMPT),
        ("human", "Generate full content for the module described above."),
    ])

    chain = prompt | llm
    result = chain.invoke({
        "topic": req.topic,
        "module_title": req.module_title,
        "level": req.level,
    })

    try:
        content = _extract_json(result.content)
    except json.JSONDecodeError:
        content = {"raw": result.content, "parse_error": "Could not parse JSON — raw output returned"}

    return content

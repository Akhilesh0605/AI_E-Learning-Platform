from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents import (
    teaching_agent,
    course_agent,
    quiz_agent,
    notes_agent,
    question_predictor,
)

app = FastAPI(
    title="Smart E-Learning — AI Microservice",
    description=(
        "LangChain + Groq powered agents for teaching, course generation, "
        "quiz, smart notes, and question prediction."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teaching_agent.router, prefix="/ai")
app.include_router(course_agent.router, prefix="/ai")
app.include_router(quiz_agent.router, prefix="/ai")
app.include_router(notes_agent.router, prefix="/ai")
app.include_router(question_predictor.router, prefix="/ai")


@app.get("/")
def root():
    return {"message": "AI Microservice running. Docs at /docs"}

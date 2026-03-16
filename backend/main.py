from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import chat, quiz, notes, questions, course

app = FastAPI(
    title="Smart E-Learning Platform — Backend",
    description="Gateway API that forwards requests to the AI microservice.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(course.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "E-Learning Backend running. AI service at http://localhost:8001/docs"}

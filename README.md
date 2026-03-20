# 🎓 Smart E-Learning Platform

> An AI-powered multi-agent learning platform that generates courses, quizzes, and study notes — adapting to your level in real time.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-learningwithai.streamlit.app-00d4aa?style=for-the-badge)](https://learningwithai.streamlit.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-000000?style=for-the-badge)](https://langchain.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge)](https://render.com)

---

## 🚀 Live Demo

**[learningwithai.streamlit.app](https://learningwithai.streamlit.app)**

> ⚠️ Hosted on Render free tier — first request may take ~30s to wake the service.

---

## What It Does

Most AI learning tools give you the same content regardless of who you are. This platform adapts everything — course structure, explanations, quiz difficulty, and study notes — based on your selected level.

A beginner asking "What is recursion?" gets an analogy about Russian nesting dolls.  
An advanced user gets stack frames, tail call optimization, and edge cases.

Same question. Completely different output. That's the core idea.

---

## 5 AI Agents

| Agent | Endpoint | What It Does |
|-------|----------|-------------|
| 📚 **Course Generator** | `POST /api/course/generate` | Generates full curriculum + module content + code examples in one action |
| 🎓 **Teaching Agent** | `POST /api/chat/ask` | Answers any question with level-adaptive explanations |
| 📝 **Quiz Engine** | `POST /api/quiz/generate` | Generates MCQ quizzes with per-question feedback and scoring |
| 📄 **Smart Notes** | `POST /api/notes/summarize` | Converts raw text or PDF into structured study notes |
| 🔮 **Question Predictor** | `POST /api/questions/predict` | Predicts high-probability exam questions by topic and exam type |

---

## Level Adaptation

| Level | Behavior |
|-------|----------|
| `beginner` | No jargon, real-world analogies, every term defined |
| `intermediate` | Assumes basics, focuses on *how* and *why*, worked examples |
| `advanced` | Deep internals, edge cases, tradeoffs, production patterns |

Try generating the same course topic at `beginner` vs `advanced` — the curriculum is completely different.

---

## Tech Stack

```
Frontend    →  Streamlit (deployed on Streamlit Cloud)
Backend     →  FastAPI (API gateway, deployed on Render)
AI Service  →  FastAPI + LangChain microservice (deployed on Render)
LLM         →  openai/gpt-oss-120b via OpenRouter
CI/CD       →  GitHub Actions + Render auto-deploy + Streamlit Cloud
```

### Architecture

```
User (Streamlit)
      │
      ▼
FastAPI Backend                 ← API gateway, request validation
https://ai-e-learning-backend.onrender.com
      │
      ▼
AI Microservice                 ← LangChain agents, LLM calls
https://e-learning-aiservice.onrender.com
      │
      ▼
OpenRouter (openai/gpt-oss-120b) ← LLM inference
```

---

## Project Structure

```
AI_E-Learning-Platform/
├── backend/                   # FastAPI gateway
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── chat.py
│       ├── quiz.py
│       ├── notes.py
│       ├── questions.py
│       └── course.py
├── ai_service/                # LangChain AI microservice
│   ├── main.py
│   └── agents/
│       ├── teaching_agent.py
│       ├── course_agent.py
│       ├── quiz_agent.py
│       ├── notes_agent.py
│       └── question_predictor.py
├── streamlit.py               # Streamlit frontend
├── .env.example
├── requirements.txt
└── start.sh                   # Local dev launcher
```

---

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/Akhilesh0605/AI_E-Learning-Platform.git
cd AI_E-Learning-Platform
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
cp .env.example .env
# Add your API keys to .env
```

```env
OPENROUTER_API_KEY=your_key_here
```

### 3. Run both services

```bash
bash start.sh
```

Or separately:

```bash
# Terminal 1 — AI Microservice
uvicorn ai_service.main:app --port 8001 --reload

# Terminal 2 — Backend Gateway
uvicorn backend.main:app --port 8000 --reload

# Terminal 3 — Streamlit Frontend
streamlit run streamlit.py
```

### 4. Open

- Streamlit UI: `http://localhost:8501`
- Backend docs: `http://localhost:8000/docs`
- AI service docs: `http://localhost:8001/docs`

---

## API Examples

### Generate a full course
```bash
curl -X POST https://ai-e-learning-backend.onrender.com/api/course/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python", "level": "beginner", "num_modules": 5}'
```

### Ask the Teaching Agent
```bash
curl -X POST https://ai-e-learning-backend.onrender.com/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is recursion?", "subject": "cs", "level": "intermediate"}'
```

### Generate a quiz
```bash
curl -X POST https://ai-e-learning-backend.onrender.com/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Binary Trees", "num_questions": 5, "difficulty": "medium"}'
```

---

## Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Streamlit Frontend | Streamlit Cloud | [learningwithai.streamlit.app](https://learningwithai.streamlit.app) |
| FastAPI Backend | Render | https://ai-e-learning-backend.onrender.com |
| AI Microservice | Render | https://e-learning-aiservice.onrender.com |

CI/CD: Both Render services auto-deploy on every push to `main`. Streamlit Cloud deploys automatically on push.

---

## Roadmap

- [x] 5 AI agents with level adaptation
- [x] Full course generation pipeline
- [x] Stateful MCQ quiz with scoring
- [x] PDF → Smart Notes pipeline
- [x] CI/CD deployment (GitHub Actions + Render + Streamlit Cloud)
- [ ] LangGraph orchestration for parallel agent execution
- [ ] OCR pipeline — photograph handwritten notes → generate course
- [ ] RAG from student's own notes (ChromaDB + sentence-transformers)
- [ ] LangSmith observability and token cost tracking
- [ ] React + Tailwind frontend rewrite

---

## Built By

**Akhilesh Kovelakuntla** — 3rd Year CS Student  
Building AI agent systems for real-world learning problems.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Akhilesh%20Kovelakuntla-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/akhilesh-kovelakuntla-09a488265)
[![GitHub](https://img.shields.io/badge/GitHub-Akhilesh0605-181717?style=flat&logo=github)](https://github.com/Akhilesh0605)
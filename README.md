# Smart E-Learning Platform

An AI-powered backend platform with **5 intelligent agents** built on LangChain + Groq (llama3-70b-8192).

---

## Project Structure

```
elearning-platform/
├── backend/                   # FastAPI gateway (port 8000)
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── chat.py
│       ├── quiz.py
│       ├── notes.py
│       ├── questions.py
│       └── course.py
├── ai_service/                # LangChain AI microservice (port 8001)
│   ├── main.py
│   └── agents/
│       ├── teaching_agent.py
│       ├── course_agent.py
│       ├── quiz_agent.py
│       ├── notes_agent.py
│       └── question_predictor.py
├── .env
├── requirements.txt
└── start.sh
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key
Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at https://console.groq.com

### 3. Run both services
```bash
bash start.sh
```

Or run them separately:
```bash
# Terminal 1 — AI Microservice
uvicorn ai_service.main:app --port 8001 --reload

# Terminal 2 — Backend Gateway
uvicorn backend.main:app --port 8000 --reload
```

---

## API Reference

### 🎓 Teaching Agent
**POST** `http://localhost:8001/ai/chat/ask`
```json
{ "question": "What is recursion?", "subject": "cs", "level": "beginner" }
```
Levels: `beginner` | `intermediate` | `advanced`
Subjects: `math` | `science` | `history` | `cs` | `general`

---

### 📚 Course Generator ⭐ WOW FEATURE
**POST** `http://localhost:8001/ai/course/generate`
```json
{ "topic": "Python", "level": "beginner", "num_modules": 5 }
```
Try the same topic at `beginner` vs `advanced` — completely different curricula!

**POST** `http://localhost:8001/ai/course/module-content`
```json
{ "topic": "Python", "module_title": "Functions and Scope", "level": "intermediate" }
```
Returns full module content: explanation, examples, code snippets, mini exercise.

---

### 📝 Quiz Generator & Evaluator
**POST** `http://localhost:8001/ai/quiz/generate`
```json
{ "topic": "Binary Trees", "num_questions": 5, "difficulty": "medium" }
```

**POST** `http://localhost:8001/ai/quiz/evaluate`
```json
{
  "question": "What is the time complexity of binary search?",
  "correct_answer": "O(log n)",
  "student_answer": "O(n log n)"
}
```

---

### 📄 PDF to Smart Notes
**POST** `http://localhost:8001/ai/notes/from-pdf` (multipart/form-data)
- `file`: PDF file upload
- `level`: beginner | intermediate | advanced

**POST** `http://localhost:8001/ai/notes/summarize`
```json
{ "text": "Your raw text here...", "level": "advanced" }
```

---

### 🔮 Important Questions Predictor
**POST** `http://localhost:8001/ai/predict/important-questions`
```json
{ "topic": "Operating Systems", "level": "advanced", "exam_type": "university" }
```
Exam types: `university` | `competitive` | `school`

---

## Level Behavior

| Level | Teaching Style |
|-------|---------------|
| `beginner` | No jargon, real-world analogies, define every term |
| `intermediate` | Assume basics, focus on *how* and *why*, worked examples |
| `advanced` | Deep internals, edge cases, tradeoffs, production patterns |

---

## Demo Flow (for reviewers)

1. Open **http://localhost:8001/docs**
2. Hit `/ai/course/generate` with `topic=Python, level=beginner` → see a structured 5-module course
3. Hit the same endpoint with `level=advanced` → completely different curriculum
4. Hit `/ai/course/module-content` to drill into any module
5. Hit `/ai/quiz/generate` with matching difficulty
6. Hit `/ai/predict/important-questions` for exam prep

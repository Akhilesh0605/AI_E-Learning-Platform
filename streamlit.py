import streamlit as st
import requests
import os

# ── Config ─────────────────────────────────────────────────────────────────────
AI_BASE = os.getenv("AI_BASE_URL", "http://localhost:8001")

st.set_page_config(
    page_title="Smart E-Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State Init ─────────────────────────────────────────────────────────
for _k, _v in {
    "course_data": None,
    "module_contents": {},
    "quiz_questions": None,
    "quiz_submitted": False,
    "pdf_bytes": None,
    "pdf_name": None,
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── CSS (CSS variables for easy theming) ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --accent:      #00d4aa;
  --accent-dim:  #00d4aa22;
  --accent-mid:  #00d4aa44;
  --accent-glow: #00d4aa33;
  --bg-base:     #0a0a0f;
  --bg-card:     #12121f;
  --bg-sidebar:  #0f0f1a;
  --bg-raised:   #1a1a2e;
  --border:      #2a2a4a;
  --text-primary:#e8e8f0;
  --text-muted:  #8888aa;
  --danger:      #ff6b6b;
  --danger-dim:  #ff6b6b15;
  --danger-mid:  #ff6b6b44;
}

html, body, [class*="css"]          { font-family: 'DM Sans', sans-serif; }
h1, h2, h3                          { font-family: 'Syne', sans-serif !important; }
.stApp                              { background: var(--bg-base); color: var(--text-primary); }
section[data-testid="stSidebar"]    { background: var(--bg-sidebar) !important; border-right: 1px solid var(--border); }

.agent-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-raised) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}

.result-box {
    background: var(--bg-card);
    border: 1px solid var(--accent-glow);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 16px;
    margin-top: 12px;
}

.tag {
    display: inline-block;
    background: var(--accent-dim);
    color: var(--accent);
    border: 1px solid var(--accent-mid);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
    margin: 2px;
}

.metric-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}

.score-display {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    margin-bottom: 20px;
}

.correct-answer {
    background: var(--accent-dim);
    border: 1px solid var(--accent-mid);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 4px 0;
}

.wrong-answer {
    background: var(--danger-dim);
    border: 1px solid var(--danger-mid);
    border-left: 3px solid var(--danger);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 4px 0;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #0099ff) !important;
    color: var(--bg-base) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 28px !important;
    letter-spacing: 0.5px;
}
.stButton > button:hover    { opacity: 0.85 !important; transform: translateY(-1px); }
.stButton > button:disabled { opacity: 0.4 !important; transform: none !important; }

.stSelectbox label, .stTextInput label,
.stTextArea label, .stSlider label {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ── API Helper ─────────────────────────────────────────────────────────────────
def api_post(endpoint, **kwargs):
    """POST to backend with structured error handling.
    Returns (data_dict, error_string). One of them is always None."""
    try:
        r = requests.post(f"{AI_BASE}{endpoint}", timeout=90, **kwargs)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to the backend. Make sure uvicorn is running on port 8001."
    except requests.exceptions.Timeout:
        return None, "Request timed out — the AI is taking too long. Try again or reduce the number of modules/questions."
    except requests.exceptions.HTTPError as e:
        body = e.response.text[:300] if e.response else ""
        return None, f"Server error {e.response.status_code}: {body}"
    except ValueError:
        return None, "Backend returned invalid JSON. Try again."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def backend_online():
    try:
        return requests.get(f"{AI_BASE}/", timeout=2).ok
    except Exception:
        return False


def _clear_quiz_answers(questions):
    """Remove radio button state keys for a question list."""
    for q in (questions or []):
        key = f"q_ans_{q.get('question_number')}"
        st.session_state.pop(key, None)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 E-Learning AI")
    st.markdown("---")
    page = st.radio(
        "Choose Agent",
        [
            "🏠 Home",
            "📚 Course Generator",
            "🎓 Teaching Agent",
            "📝 Quiz Generator",
            "📄 Smart Notes",
            "🔮 Question Predictor",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**AI Service**")
    if backend_online():
        st.success("🟢 Connected")
    else:
        st.error("🔴 Offline — start uvicorn on port 8001")


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("# Smart E-Learning Platform")
    st.markdown("#### AI-powered learning with 5 intelligent agents")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-box">
            <h2 style='color:var(--accent);font-family:Syne,sans-serif;margin:0'>5</h2>
            <p style='color:var(--text-muted);margin:4px 0 0'>AI Agents</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-box">
            <h2 style='color:var(--accent);font-family:Syne,sans-serif;margin:0'>3</h2>
            <p style='color:var(--text-muted);margin:4px 0 0'>Learning Levels</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-box">
            <h2 style='color:var(--accent);font-family:Syne,sans-serif;margin:0'>Groq</h2>
            <p style='color:var(--text-muted);margin:4px 0 0'>AI Backend</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Agents")

    for icon, name, desc in [
        ("📚", "Course Generator",
         "Generates a full structured course — curriculum + detailed module content + code examples — automatically."),
        ("🎓", "Teaching Agent",
         "Ask any question on any subject. Explanation style adapts to your level."),
        ("📝", "Quiz Generator",
         "MCQ quizzes with interactive answer selection. Reveals results only after you submit."),
        ("📄", "Smart Notes",
         "Paste text or upload a PDF — get smart study notes styled for your level."),
        ("🔮", "Question Predictor",
         "Predict important exam questions by topic, level, and exam type with marks weightage."),
    ]:
        st.markdown(f"""<div class="agent-card">
            <h4 style='font-family:Syne,sans-serif;color:var(--text-primary);margin:0 0 6px'>{icon} {name}</h4>
            <p style='color:var(--text-muted);margin:0;font-size:14px'>{desc}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# COURSE GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📚 Course Generator":
    st.markdown("# 📚 Course Generator")
    st.markdown("Generates the full course structure **and** detailed module content automatically.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Generate Full Course", "Module Deep Dive"])

    # ── Tab 1: Full course ──
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            topic = st.text_input("Topic", value="Python Programming")
        with col2:
            level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
        with col3:
            num_modules = st.slider("Modules", 3, 10, 5)

        if st.button("Generate Full Course ✨"):
            # Reset previous results
            st.session_state.course_data = None
            st.session_state.module_contents = {}

            # Step 1 — Course structure
            with st.spinner("Designing curriculum structure..."):
                data, err = api_post("/api/course/generate", json={
                    "topic": topic, "level": level, "num_modules": num_modules
                })

            if err:
                st.error(err)
            elif "parse_error" in data:
                st.error("AI returned an unexpected format. Please try again.")
            else:
                st.session_state.course_data = data

                # Step 2 — Auto-generate content for every module
                modules = data.get("modules", [])
                prog = st.progress(0, text="Generating module content...")
                for i, mod in enumerate(modules):
                    prog.progress(
                        (i + 1) / len(modules),
                        text=f"Module {mod.get('module_number')}: {mod.get('title')}..."
                    )
                    mc_data, mc_err = api_post("/api/course/module-content", json={
                        "topic": topic,
                        "module_title": mod.get("title", ""),
                        "level": level,
                    })
                    if not mc_err and mc_data and "parse_error" not in mc_data:
                        st.session_state.module_contents[mod.get("module_number")] = mc_data

                prog.empty()
                loaded = len(st.session_state.module_contents)
                st.success(f"✅ Course ready — {loaded}/{len(modules)} modules fully loaded!")
                st.rerun()

        # ── Display stored course ──
        if st.session_state.course_data:
            d = st.session_state.course_data
            st.markdown(f"### {d.get('course_title', 'Course')}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Level:** `{d.get('level', '')}`")
                st.markdown(f"**Total modules:** {d.get('total_modules', '')}")
            with col_b:
                prereqs = d.get("prerequisites", [])
                if prereqs:
                    st.markdown("**Prerequisites:** " + " ".join(
                        [f"<span class='tag'>{p}</span>" for p in prereqs]
                    ), unsafe_allow_html=True)

            st.markdown("---")

            for mod in d.get("modules", []):
                mnum = mod.get("module_number")
                mc = st.session_state.module_contents.get(mnum)

                with st.expander(f"Module {mnum} — {mod.get('title')}"):
                    # Structure info
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.markdown(f"**Time:** {mod.get('estimated_time')}")
                        st.markdown(f"**Difficulty:** {mod.get('difficulty_score')}/10")
                    with col_y:
                        st.markdown(f"**Description:** {mod.get('description')}")

                    topics = mod.get("topics_covered", [])
                    if topics:
                        st.markdown("**Topics:** " + " ".join(
                            [f"<span class='tag'>{t}</span>" for t in topics]
                        ), unsafe_allow_html=True)

                    outcomes = mod.get("learning_outcomes", [])
                    if outcomes:
                        st.markdown("**Outcomes:**")
                        for o in outcomes:
                            st.markdown(f"- {o}")

                    # Module content (auto-generated)
                    if mc:
                        st.markdown("---")
                        st.markdown("##### Overview")
                        st.markdown(mc.get("overview", ""))

                        concepts = mc.get("key_concepts", [])
                        if concepts:
                            st.markdown("**Key Concepts:** " + " ".join(
                                [f"<span class='tag'>{c}</span>" for c in concepts]
                            ), unsafe_allow_html=True)

                        st.markdown("##### Detailed Explanation")
                        st.markdown(mc.get("detailed_explanation", ""))

                        snippets = mc.get("code_snippets", [])
                        if snippets:
                            st.markdown("##### Code Examples")
                            for s in snippets:
                                st.code(s, language="python")

                        exercise = mc.get("mini_exercise", {})
                        if exercise:
                            st.markdown("##### 💪 Mini Exercise")
                            st.markdown(exercise.get("description", ""))
                            hints = exercise.get("hints", [])
                            if hints:
                                with st.expander("Hints"):
                                    for h in hints:
                                        st.markdown(f"- {h}")
                    else:
                        st.caption("Module content not loaded — try regenerating the course.")

            project = d.get("final_project_idea")
            if project:
                st.markdown("---")
                st.markdown(f"### 🚀 Final Project\n{project}")

    # ── Tab 2: Manual module deep-dive ──
    with tab2:
        st.markdown("Fetch detailed content for any specific module.")
        col1, col2 = st.columns(2)
        with col1:
            mc_topic  = st.text_input("Course Topic", value="Python Programming", key="mc_topic")
            mc_module = st.text_input("Module Title", value="Functions and Scope")
        with col2:
            mc_level = st.selectbox("Level", ["beginner", "intermediate", "advanced"], key="mc_level")

        if st.button("Get Module Content 📖"):
            with st.spinner("Generating module content..."):
                data, err = api_post("/api/course/module-content", json={
                    "topic": mc_topic, "module_title": mc_module, "level": mc_level
                })

            if err:
                st.error(err)
            elif "parse_error" in data:
                st.error("AI returned an unexpected format. Please try again.")
            else:
                st.markdown(f"### {data.get('module_title', mc_module)}")
                st.markdown(data.get("overview", ""))

                concepts = data.get("key_concepts", [])
                if concepts:
                    st.markdown("**Key Concepts:** " + " ".join(
                        [f"<span class='tag'>{c}</span>" for c in concepts]
                    ), unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### Explanation")
                st.markdown(data.get("detailed_explanation", ""))

                snippets = data.get("code_snippets", [])
                if snippets:
                    st.markdown("### Code Examples")
                    for s in snippets:
                        st.code(s, language="python")

                exercise = data.get("mini_exercise", {})
                if exercise:
                    st.markdown("### 💪 Mini Exercise")
                    st.markdown(exercise.get("description", ""))
                    hints = exercise.get("hints", [])
                    if hints:
                        with st.expander("Hints"):
                            for h in hints:
                                st.markdown(f"- {h}")


# ══════════════════════════════════════════════════════════════════════════════
# TEACHING AGENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎓 Teaching Agent":
    st.markdown("# 🎓 Teaching Agent")
    st.markdown("Ask anything — the explanation adapts to your level.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        question = st.text_area("Your Question", value="What is recursion?", height=100)
    with col2:
        subject = st.selectbox("Subject", ["cs", "math", "science", "history", "general"])
        level   = st.selectbox("Level",   ["beginner", "intermediate", "advanced"])
    with col3:
        st.markdown("**Level Guide**")
        st.markdown("🟢 **Beginner** — analogies, no jargon")
        st.markdown("🟡 **Intermediate** — concepts + examples")
        st.markdown("🔴 **Advanced** — deep theory + edge cases")

    if st.button("Ask AI 🤖"):
        with st.spinner("Thinking..."):
            data, err = api_post("/api/chat", json={
                "question": question, "subject": subject, "level": level
            })
        if err:
            st.error(err)
        else:
            st.markdown("---")
            # Render as plain markdown — avoids XSS from untrusted API content
            with st.container(border=True):
                st.markdown(data.get("answer", ""))


# ══════════════════════════════════════════════════════════════════════════════
# QUIZ GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Quiz Generator":
    st.markdown("# 📝 Quiz Generator")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Take a Quiz", "Evaluate Open Answer"])

    # ── Tab 1: Interactive MCQ quiz ──
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            q_topic = st.text_input("Topic", value="Binary Trees")
        with col2:
            q_diff = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        with col3:
            q_num = st.slider("Questions", 3, 10, 5)

        if st.button("Generate Quiz 📝"):
            with st.spinner("Generating questions..."):
                data, err = api_post("/api/quiz/generate", json={
                    "topic": q_topic, "num_questions": q_num, "difficulty": q_diff
                })
            if err:
                st.error(err)
            elif "parse_error" in data:
                st.error("AI returned an unexpected format. Please try again.")
            else:
                questions = data.get("questions", [])
                if questions:
                    _clear_quiz_answers(st.session_state.quiz_questions)  # clear old answers
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_submitted = False
                    st.rerun()
                else:
                    st.warning("No questions were returned. Try again.")

        # ── Quiz in progress ──
        if st.session_state.quiz_questions:
            questions = st.session_state.quiz_questions

            if not st.session_state.quiz_submitted:
                st.markdown("---")
                st.markdown(f"### Answer all {len(questions)} questions, then click **Submit Quiz**.")

                for q in questions:
                    qnum = q.get("question_number")
                    opts = q.get("options", {})
                    option_labels = [f"{k}. {v}" for k, v in opts.items()]

                    st.markdown(f"**Q{qnum}. {q.get('question')}**")
                    st.radio(
                        "Select your answer",
                        option_labels,
                        key=f"q_ans_{qnum}",
                        index=None,              # no pre-selection
                        label_visibility="collapsed",
                    )
                    st.markdown("")   # spacer

                # Check all answered
                all_answered = all(
                    st.session_state.get(f"q_ans_{q.get('question_number')}") is not None
                    for q in questions
                )

                if not all_answered:
                    st.info("Select an answer for every question to enable submission.")

                if st.button("Submit Quiz ✅", disabled=not all_answered):
                    st.session_state.quiz_submitted = True
                    st.rerun()

            # ── Results view ──
            else:
                correct_count = 0
                results = []

                for q in questions:
                    qnum        = q.get("question_number")
                    correct_key = q.get("correct_answer", "")       # e.g. "A"
                    user_raw    = st.session_state.get(f"q_ans_{qnum}", "") or ""
                    user_letter = user_raw[0] if user_raw else ""   # first char = "A"/"B"/…
                    is_correct  = user_letter == correct_key
                    if is_correct:
                        correct_count += 1
                    results.append({
                        "q": q,
                        "user_letter": user_letter,
                        "is_correct": is_correct,
                    })

                score_pct = int((correct_count / len(questions)) * 100)
                color     = "var(--accent)" if score_pct >= 70 else "var(--danger)"
                emoji     = "🎉" if score_pct >= 70 else "💪"
                message   = "Great job!" if score_pct >= 70 else "Keep practicing!"

                st.markdown(f"""<div class="score-display">
                    <h2 style='color:{color};font-family:Syne,sans-serif;margin:0'>
                        {correct_count} / {len(questions)} &nbsp;·&nbsp; {score_pct}%
                    </h2>
                    <p style='color:var(--text-muted);margin:8px 0 0'>{message} {emoji}</p>
                </div>""", unsafe_allow_html=True)

                st.markdown("### Review")

                for r in results:
                    q           = r["q"]
                    qnum        = q.get("question_number")
                    user_letter = r["user_letter"]
                    is_correct  = r["is_correct"]
                    correct_key = q.get("correct_answer", "")
                    opts        = q.get("options", {})
                    icon        = "✅" if is_correct else "❌"

                    with st.expander(f"{icon} Q{qnum}. {q.get('question')}"):
                        for k, v in opts.items():
                            markers = ""
                            if k == user_letter:
                                markers += " ← **your answer**"
                            if k == correct_key:
                                markers += " ✅"
                            st.markdown(f"**{k}.** {v}{markers}")

                        if not is_correct:
                            st.markdown(
                                f"<div class='correct-answer'>✅ Correct answer: "
                                f"<strong>{correct_key}.</strong> {opts.get(correct_key, '')}</div>",
                                unsafe_allow_html=True,
                            )
                        st.markdown(f"💡 **Explanation:** {q.get('explanation', '')}")

                st.markdown("---")
                if st.button("Retake Quiz 🔄"):
                    _clear_quiz_answers(questions)
                    st.session_state.quiz_submitted = False
                    st.rerun()

                if st.button("New Quiz 🆕"):
                    _clear_quiz_answers(questions)
                    st.session_state.quiz_questions = None
                    st.session_state.quiz_submitted = False
                    st.rerun()

    # ── Tab 2: Open-answer evaluator ──
    with tab2:
        st.markdown("Evaluate a student's free-text answer against a model answer.")
        eq = st.text_input("Question", value="What is the time complexity of binary search?")
        col1, col2 = st.columns(2)
        with col1:
            correct = st.text_input("Correct Answer", value="O(log n)")
        with col2:
            student = st.text_input("Student Answer", value="O(n log n)")

        if st.button("Evaluate ✅"):
            with st.spinner("Evaluating..."):
                data, err = api_post("/api/quiz/evaluate", json={
                    "question": eq, "correct_answer": correct, "student_answer": student
                })
            if err:
                st.error(err)
            else:
                score = data.get("score", 0)
                color = "var(--accent)" if score >= 70 else "var(--danger)"
                st.markdown(f"""<div class="score-display">
                    <h3 style='color:{color};font-family:Syne,sans-serif;margin:0'>Score: {score}/100</h3>
                    <p style='margin:8px 0 0'>{data.get('feedback', '')}</p>
                </div>""", unsafe_allow_html=True)
                missed = data.get("key_points_missed", [])
                if missed:
                    st.markdown("**Points missed:**")
                    for m in missed:
                        st.markdown(f"- {m}")


# ══════════════════════════════════════════════════════════════════════════════
# SMART NOTES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Smart Notes":
    st.markdown("# 📄 Smart Notes")
    st.markdown("---")

    tab1, tab2 = st.tabs(["From Text", "From PDF"])

    with tab1:
        text_input = st.text_area(
            "Paste your text here", height=200,
            value="A neural network is a series of algorithms that attempt to recognize "
                  "underlying relationships in a set of data through a process that mimics "
                  "the way the human brain operates.",
        )
        n_level = st.selectbox("Notes Level", ["beginner", "intermediate", "advanced"])

        if st.button("Generate Notes 📄"):
            with st.spinner("Generating notes..."):
                data, err = api_post("/api/notes/summarize", json={
                    "text": text_input, "level": n_level
                })
            if err:
                st.error(err)
            else:
                st.markdown("---")
                st.markdown(data.get("notes", ""))

    with tab2:
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        # Cache bytes so re-runs don't clear the file
        if uploaded is not None:
            st.session_state.pdf_bytes = uploaded.read()
            st.session_state.pdf_name  = uploaded.name

        pdf_level = st.selectbox(
            "Notes Level", ["beginner", "intermediate", "advanced"], key="pdf_level"
        )

        if st.session_state.pdf_bytes:
            st.caption(f"📎 Loaded: {st.session_state.pdf_name}")

            if st.button("Extract Notes 📑"):
                with st.spinner("Extracting and summarising PDF..."):
                    data, err = api_post(
                        "/api/notes/from-pdf",
                        files={"file": (
                            st.session_state.pdf_name,
                            st.session_state.pdf_bytes,
                            "application/pdf",
                        )},
                        data={"level": pdf_level},
                    )
                if err:
                    st.error(err)
                elif "error" in data:
                    st.error(data["error"])
                else:
                    st.markdown(
                        f"**Source:** {data.get('source')} &nbsp;|&nbsp; "
                        f"**Chars processed:** {data.get('characters_processed')}",
                        unsafe_allow_html=True,
                    )
                    st.markdown("---")
                    st.markdown(data.get("notes", ""))
        else:
            st.info("Upload a PDF to get started.")


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Question Predictor":
    st.markdown("# 🔮 Question Predictor")
    st.markdown("Predict important exam questions before you sit the exam.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        p_topic = st.text_input("Topic", value="Operating Systems")
    with col2:
        p_level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
    with col3:
        p_exam = st.selectbox("Exam Type", ["university", "competitive", "school"])

    if st.button("Predict Questions 🔮"):
        with st.spinner("Analysing exam patterns..."):
            data, err = api_post("/api/questions/predict", json={
                "topic": p_topic, "level": p_level, "exam_type": p_exam
            })
        if err:
            st.error(err)
        elif "parse_error" in data:
            st.error("AI returned an unexpected format. Please try again.")
        else:
            priority = data.get("high_priority_topics", [])
            if priority:
                st.markdown(
                    "**High Priority Topics:** " + " ".join(
                        [f"<span class='tag'>{t}</span>" for t in priority]
                    ), unsafe_allow_html=True,
                )

            tip = data.get("study_tip")
            if tip:
                st.info(f"💡 {tip}")

            st.markdown("---")
            st.markdown("### Predicted Questions")

            for q in data.get("predicted_questions", []):
                with st.expander(f"Q{q.get('question_number')}. {q.get('question')}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Type:** `{q.get('question_type')}`")
                        st.markdown(f"**Marks:** {q.get('marks_weightage')}")
                    with col_b:
                        st.markdown(f"**Why important:** {q.get('reason_for_importance')}")
                    hint = q.get("hint")
                    if hint:
                        st.markdown(f"💡 **Hint:** {hint}")
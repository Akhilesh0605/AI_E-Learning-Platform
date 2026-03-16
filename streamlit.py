import streamlit as st
import requests
import json

AI_BASE = "http://localhost:8001"

st.set_page_config(
    page_title="Smart E-Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e2e;
}

.agent-card {
    background: linear-gradient(135deg, #12121f 0%, #1a1a2e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}

.result-box {
    background: #0f0f1a;
    border: 1px solid #00d4aa33;
    border-left: 3px solid #00d4aa;
    border-radius: 8px;
    padding: 16px;
    margin-top: 12px;
}

.tag {
    display: inline-block;
    background: #00d4aa22;
    color: #00d4aa;
    border: 1px solid #00d4aa44;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
    margin: 2px;
}

.module-card {
    background: #12121f;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 14px;
    margin: 8px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #0099ff) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 28px !important;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px);
}

.stSelectbox label, .stTextInput label, .stTextArea label, .stSlider label {
    color: #8888aa !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.metric-box {
    background: #12121f;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
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
    try:
        r = requests.get(f"{AI_BASE}/", timeout=2)
        st.success("🟢 Connected")
    except:
        st.error("🔴 Offline — start uvicorn on port 8001")


# ── Home ──────────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("# Smart E-Learning Platform")
    st.markdown("#### AI-powered learning with 5 intelligent agents")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-box">
            <h2 style='color:#00d4aa;font-family:Syne,sans-serif;margin:0'>5</h2>
            <p style='color:#8888aa;margin:4px 0 0'>AI Agents</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-box">
            <h2 style='color:#00d4aa;font-family:Syne,sans-serif;margin:0'>3</h2>
            <p style='color:#8888aa;margin:4px 0 0'>Learning Levels</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-box">
            <h2 style='color:#00d4aa;font-family:Syne,sans-serif;margin:0'>gpt-120b</h2>
            <p style='color:#8888aa;margin:4px 0 0'>Groq Model</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Agents")

    agents = [
        ("📚", "Course Generator", "Generate full structured course curricula with modules, outcomes, and project ideas. Try beginner vs advanced on the same topic."),
        ("🎓", "Teaching Agent", "Ask any question on any subject. Response style adapts based on your level — from simple analogies to deep theory."),
        ("📝", "Quiz Generator", "Auto-generate MCQ quizzes with explanations, then evaluate student answers with scoring and feedback."),
        ("📄", "Smart Notes", "Upload a PDF or paste text — get smart study notes styled for your level."),
        ("🔮", "Question Predictor", "Predict important exam questions by topic, level, and exam type with marks weightage."),
    ]

    for icon, name, desc in agents:
        st.markdown(f"""<div class="agent-card">
            <h4 style='font-family:Syne,sans-serif;color:#e8e8f0;margin:0 0 6px'>{icon} {name}</h4>
            <p style='color:#8888aa;margin:0;font-size:14px'>{desc}</p>
        </div>""", unsafe_allow_html=True)


# ── Course Generator ──────────────────────────────────────────────────────────
elif page == "📚 Course Generator":
    st.markdown("# 📚 Course Generator")
    st.markdown("Generate a full structured course curriculum on any topic.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Generate Course", "Module Content"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            topic = st.text_input("Topic", value="Python Programming")
        with col2:
            level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
        with col3:
            num_modules = st.slider("Modules", 3, 10, 5)

        if st.button("Generate Course ✨"):
            with st.spinner("Designing curriculum..."):
                try:
                    r = requests.post(f"{AI_BASE}/ai/course/generate", json={
                        "topic": topic, "level": level, "num_modules": num_modules
                    }, timeout=60)
                    data = r.json()

                    if "parse_error" in data:
                        st.error("AI returned invalid JSON. Try again.")
                        st.code(data.get("raw", ""))
                    else:
                        st.markdown(f"### {data.get('course_title', topic)}")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**Level:** `{data.get('level', level)}`")
                            st.markdown(f"**Modules:** {data.get('total_modules', num_modules)}")
                        with col_b:
                            prereqs = data.get("prerequisites", [])
                            if prereqs:
                                st.markdown("**Prerequisites:**")
                                for p in prereqs:
                                    st.markdown(f"<span class='tag'>{p}</span>", unsafe_allow_html=True)

                        st.markdown("---")
                        st.markdown("### Modules")
                        for mod in data.get("modules", []):
                            with st.expander(f"Module {mod.get('module_number')} — {mod.get('title')}"):
                                st.markdown(f"**Description:** {mod.get('description')}")
                                st.markdown(f"**Estimated Time:** {mod.get('estimated_time')} &nbsp; **Difficulty:** {mod.get('difficulty_score')}/10", unsafe_allow_html=True)
                                topics = mod.get("topics_covered", [])
                                if topics:
                                    st.markdown("**Topics:** " + " ".join([f"<span class='tag'>{t}</span>" for t in topics]), unsafe_allow_html=True)
                                outcomes = mod.get("learning_outcomes", [])
                                if outcomes:
                                    st.markdown("**Outcomes:**")
                                    for o in outcomes:
                                        st.markdown(f"- {o}")

                        project = data.get("final_project_idea")
                        if project:
                            st.markdown("---")
                            st.markdown(f"### 🚀 Final Project\n{project}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            mc_topic = st.text_input("Course Topic", value="Python Programming", key="mc_topic")
            mc_module = st.text_input("Module Title", value="Functions and Scope")
        with col2:
            mc_level = st.selectbox("Level", ["beginner", "intermediate", "advanced"], key="mc_level")

        if st.button("Get Module Content 📖"):
            with st.spinner("Generating module content..."):
                try:
                    r = requests.post(f"{AI_BASE}/ai/course/module-content", json={
                        "topic": mc_topic, "module_title": mc_module, "level": mc_level
                    }, timeout=60)
                    data = r.json()

                    if "parse_error" in data:
                        st.error("AI returned invalid JSON.")
                        st.code(data.get("raw", ""))
                    else:
                        st.markdown(f"### {data.get('module_title', mc_module)}")
                        st.markdown(data.get("overview", ""))

                        concepts = data.get("key_concepts", [])
                        if concepts:
                            st.markdown("**Key Concepts:** " + " ".join([f"<span class='tag'>{c}</span>" for c in concepts]), unsafe_allow_html=True)

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
                except Exception as e:
                    st.error(f"Error: {e}")


# ── Teaching Agent ────────────────────────────────────────────────────────────
elif page == "🎓 Teaching Agent":
    st.markdown("# 🎓 Teaching Agent")
    st.markdown("Ask anything — the explanation adapts to your level.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        question = st.text_area("Your Question", value="What is recursion?", height=100)
    with col2:
        subject = st.selectbox("Subject", ["cs", "math", "science", "history", "general"])
        level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
    with col3:
        st.markdown("**Level Guide**")
        st.markdown("🟢 **Beginner** — analogies, no jargon")
        st.markdown("🟡 **Intermediate** — concepts + examples")
        st.markdown("🔴 **Advanced** — deep theory + edge cases")

    if st.button("Ask AI 🤖"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(f"{AI_BASE}/ai/chat/ask", json={
                    "question": question, "subject": subject, "level": level
                }, timeout=60)
                data = r.json()
                st.markdown("---")
                st.markdown(f"<div class='result-box'>{data.get('answer', '')}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


# ── Quiz ──────────────────────────────────────────────────────────────────────
elif page == "📝 Quiz Generator":
    st.markdown("# 📝 Quiz Generator")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Generate Quiz", "Evaluate Answer"])

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
                try:
                    r = requests.post(f"{AI_BASE}/ai/quiz/generate", json={
                        "topic": q_topic, "num_questions": q_num, "difficulty": q_diff
                    }, timeout=60)
                    data = r.json()

                    if "parse_error" in data:
                        st.error("Could not parse quiz.")
                        st.code(data.get("raw", ""))
                    else:
                        questions = data.get("questions", [])
                        for q in questions:
                            with st.expander(f"Q{q.get('question_number')}. {q.get('question')}"):
                                opts = q.get("options", {})
                                for k, v in opts.items():
                                    st.markdown(f"**{k}.** {v}")
                                st.markdown(f"✅ **Answer:** {q.get('correct_answer')}")
                                st.markdown(f"💡 **Explanation:** {q.get('explanation')}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        eq = st.text_input("Question", value="What is the time complexity of binary search?")
        col1, col2 = st.columns(2)
        with col1:
            correct = st.text_input("Correct Answer", value="O(log n)")
        with col2:
            student = st.text_input("Student Answer", value="O(n log n)")

        if st.button("Evaluate ✅"):
            with st.spinner("Evaluating..."):
                try:
                    r = requests.post(f"{AI_BASE}/ai/quiz/evaluate", json={
                        "question": eq, "correct_answer": correct, "student_answer": student
                    }, timeout=60)
                    data = r.json()
                    score = data.get("score", 0)
                    color = "#00d4aa" if score >= 70 else "#ff6b6b"
                    st.markdown(f"""<div class='result-box'>
                        <h3 style='color:{color};font-family:Syne,sans-serif'>Score: {score}/100</h3>
                        <p>{data.get('feedback', '')}</p>
                    </div>""", unsafe_allow_html=True)
                    missed = data.get("key_points_missed", [])
                    if missed:
                        st.markdown("**Points missed:**")
                        for m in missed:
                            st.markdown(f"- {m}")
                except Exception as e:
                    st.error(f"Error: {e}")


# ── Smart Notes ───────────────────────────────────────────────────────────────
elif page == "📄 Smart Notes":
    st.markdown("# 📄 Smart Notes")
    st.markdown("---")

    tab1, tab2 = st.tabs(["From Text", "From PDF"])

    with tab1:
        text_input = st.text_area("Paste your text here", height=200,
            value="A neural network is a series of algorithms that attempt to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.")
        n_level = st.selectbox("Notes Level", ["beginner", "intermediate", "advanced"])

        if st.button("Generate Notes 📄"):
            with st.spinner("Generating notes..."):
                try:
                    r = requests.post(f"{AI_BASE}/ai/notes/summarize", json={
                        "text": text_input, "level": n_level
                    }, timeout=60)
                    data = r.json()
                    st.markdown("---")
                    st.markdown(data.get("notes", ""))
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        pdf_level = st.selectbox("Notes Level", ["beginner", "intermediate", "advanced"], key="pdf_level")

        if uploaded and st.button("Extract Notes 📑"):
            with st.spinner("Extracting and summarizing PDF..."):
                try:
                    r = requests.post(
                        f"{AI_BASE}/ai/notes/from-pdf",
                        files={"file": (uploaded.name, uploaded.read(), "application/pdf")},
                        data={"level": pdf_level},
                        timeout=120
                    )
                    data = r.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.markdown(f"**Source:** {data.get('source')} | **Chars processed:** {data.get('characters_processed')}")
                        st.markdown("---")
                        st.markdown(data.get("notes", ""))
                except Exception as e:
                    st.error(f"Error: {e}")


# ── Question Predictor ────────────────────────────────────────────────────────
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
        with st.spinner("Analyzing exam patterns..."):
            try:
                r = requests.post(f"{AI_BASE}/ai/predict/important-questions", json={
                    "topic": p_topic, "level": p_level, "exam_type": p_exam
                }, timeout=60)
                data = r.json()

                if "parse_error" in data:
                    st.error("Could not parse predictions.")
                    st.code(data.get("raw", ""))
                else:
                    priority = data.get("high_priority_topics", [])
                    if priority:
                        st.markdown("**High Priority Topics:** " + " ".join([f"<span class='tag'>{t}</span>" for t in priority]), unsafe_allow_html=True)

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
            except Exception as e:
                st.error(f"Error: {e}")
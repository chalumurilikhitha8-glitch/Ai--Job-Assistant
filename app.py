import re
import streamlit as st

st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Application Assistant")
st.write("Analyze your resume against a job description and generate insights.")

resume = st.text_area("📄 Paste Resume Here", height=250)
job = st.text_area("📌 Paste Job Description Here", height=250)

STOPWORDS = {
    "the", "and", "for", "with", "you", "your", "are", "this", "that", "from",
    "have", "will", "our", "job", "role", "all", "not", "but", "can", "use",
    "has", "any", "who", "their", "they", "his", "her", "she", "him", "its",
    "was", "were", "had", "been", "able", "into", "out", "about", "than",
    "then", "them", "also", "such", "including", "across", "through", "using",
    "work", "works", "working", "experience", "candidate", "resume", "description",
    "apply", "application", "applications", "company", "companies",
    "opportunity", "opportunities", "required", "preferred", "strong", "good",
    "well", "position", "knowledge", "ability", "abilities"
}

IMPORTANT_KEYWORDS = [
    "python",
    "sql",
    "power bi",
    "tableau",
    "excel",
    "salesforce",
    "crm",
    "prompt engineering",
    "generative ai",
    "llm",
    "llms",
    "api",
    "apis",
    "langchain",
    "rag",
    "vector database",
    "vector databases",
    "embeddings",
    "automation",
    "analytics",
    "data analysis",
    "machine learning",
    "ai agents",
    "agentic ai",
    "streamlit",
    "communication",
    "documentation",
    "problem solving",
    "stakeholder",
    "collaboration",
    "workflow",
    "reporting",
    "dashboard",
    "business analysis",
    "retrieval augmented generation",
    "large language models",
    "customer relationship management",
    "process improvement",
    "cybersecurity",
    "google workspace",
    "microsoft 365",
    "windows",
    "troubleshooting",
    "hardware",
    "software",
    "customer service",
    "technical support",
    "incident management",
    "ticketing",
    "it support"
]

GENERIC_WORDS = {
    "workflow",
    "process",
    "improvement",
    "technology",
    "systems",
    "practices",
    "solutions",
    "service",
    "support"
}

BAD_WORDS = {
    "members", "staff", "team", "teams", "role", "job",
    "technical", "tools", "experience", "expertise",
    "administration", "attention", "collaborative",
    "process", "improvement", "mission", "organization",
    "helpful", "strong", "quality", "services", "while",
    "similar", "furthering", "technical", "microsoft"
}

def normalize_text(text):
    return text.lower().strip()

def extract_words(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9\-\+/#]*\b", text.lower())
    return [w for w in words if len(w) > 3 and w not in STOPWORDS]

def extract_phrases(text):
    text = normalize_text(text)
    found = []
    for kw in IMPORTANT_KEYWORDS:
        if kw in text:
            found.append(kw)
    return found

def dedupe_keep_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def get_fallback_keywords(word_list):
    fallback = []
    for word in word_list:
        if len(word) > 4 and word not in STOPWORDS and word.isalpha():
            fallback.append(word)
    return dedupe_keep_order(fallback)

def safe_get(items, index, default_value):
    return items[index] if len(items) > index else default_value

if st.button("Analyze"):
    if not resume.strip() or not job.strip():
        st.warning("Please enter both resume and job description.")
    else:
        resume_words = set(extract_words(resume))
        job_words = set(extract_words(job))

        resume_phrases = set(extract_phrases(resume))
        job_phrases = set(extract_phrases(job))

        matched_phrases = dedupe_keep_order(list(resume_phrases & job_phrases))
        missing_phrases = dedupe_keep_order(list(job_phrases - resume_phrases))

        matched_words = get_fallback_keywords(list(resume_words & job_words))
        missing_words = get_fallback_keywords(list(job_words - resume_words))

        matched = matched_phrases + matched_words[:5]
        missing = missing_phrases + missing_words[:5]

        matched = [m for m in matched if m not in GENERIC_WORDS and m not in BAD_WORDS]
        missing = [m for m in missing if m not in GENERIC_WORDS and m not in BAD_WORDS]

        matched = list(dict.fromkeys(matched))[:8]
        missing = list(dict.fromkeys(missing))[:8]

        if not matched:
            matched = ["communication", "problem solving", "documentation"]

        if not missing:
            missing = ["ai", "api", "automation"]

        score = round((len(matched) / (len(matched) + len(missing) + 1)) * 10, 1)

        st.subheader("📊 Analysis Result")

        if score >= 8:
            st.success(f"Match Score: {score}/10 — Strong Match")
        elif score >= 6:
            st.warning(f"Match Score: {score}/10 — Moderate Match")
        else:
            st.error(f"Match Score: {score}/10 — Low Match")

        st.progress(min(score / 10, 1.0))

        st.info("💡 Insight: Your resume partially matches the job. Focus on adding missing technical keywords and relevant project experience to improve your chances.")

        st.markdown("### 🔍 Why this score?")
        st.write(f"Your resume matches key areas like: {', '.join(matched[:3])}.")
        st.write(f"However, it is missing important areas like: {', '.join(missing[:3])}.")

        st.markdown("## 💪 Strengths (Matching Skills)")
        for item in matched[:8]:
            st.write(f"- {item}")

        st.markdown("## ⚠️ Missing Skills (Gap Analysis)")
        for item in missing[:8]:
            st.write(f"- {item}")

        st.markdown("### 🎯 Top Priority Skills to Learn")
        priority = missing[:3]
        for i, skill in enumerate(priority, 1):
            st.write(f"{i}. {skill}")

        st.markdown("### 🚀 What to improve next")
        st.success(f"To improve your match score, focus on learning and adding: {', '.join(missing[:3])}.")

        st.markdown("## 3. Suggestions")
        suggestions = [
            f"Focus first on adding or learning: {', '.join(missing[:3])}.",
            "Add missing technical keywords from the job description.",
            "Include measurable achievements such as numbers, percentages, or business impact.",
            "Highlight relevant tools, platforms, and technologies."
        ]

        for item in suggestions:
            st.write(f"- {item}")

        st.markdown("## 🧠 Project Ideas to Improve Your Resume")
        project_1 = safe_get(missing, 0, "automation")
        project_2 = safe_get(missing, 1, "api")
        project_3 = safe_get(missing, 2, "analytics")

        projects = [
            f"Build a project using {project_1} (Example: dashboard or tool).",
            f"Create a mini project using {project_2} to demonstrate practical skills.",
            f"Add a real-world use case project using {project_3}."
        ]

        for project in projects:
            st.write(f"- {project}")

        st.markdown("## ✍️ Add These Lines to Your Resume")
        improve_lines = [
            f"Developed solutions using {project_1} to improve efficiency.",
            f"Implemented workflows using {project_2} to enhance performance.",
            f"Worked on projects involving {project_3} to solve business problems."
        ]

        for line in improve_lines:
            st.write(f"- {line}")

        st.markdown("## 4. Tailored Resume Bullet Points")
        strengths_text = ", ".join(matched[:3])
        missing_text = ", ".join(missing[:3])

        bullets = [
            f"Applied strengths in {strengths_text} to support business needs and improve workflow outcomes.",
            "Collaborated with cross-functional teams to resolve issues, improve processes, and enhance user experience.",
            "Created clear documentation and structured workflows to improve consistency and operational efficiency.",
            f"Actively building capability in {missing_text} to strengthen alignment with target job requirements."
        ]

        for bullet in bullets:
            st.write(f"- {bullet}")

        st.markdown("## 5. ATS-Friendly Cover Letter")
        cover_letter = f"""Dear Hiring Manager,

I am excited to apply for this opportunity. My background includes experience in customer support, documentation, workflow improvement, and collaboration across teams. I am also actively building technical skills that align with this role.

I bring relevant strengths in {strengths_text}, along with a strong willingness to learn and adapt quickly. I am currently strengthening areas such as {missing_text} to improve my fit for advanced roles.

This opportunity strongly interests me because it aligns with my goal of using analytical thinking, communication, and technical learning to contribute meaningfully. I would welcome the opportunity to grow and contribute to your team.

Sincerely,
Your Name
"""
        st.text_area("Generated Cover Letter", value=cover_letter, height=220)

        st.markdown("## 6. Interview Tips")
        tips = [
            "Explain how your current experience transfers to the target role.",
            "Prepare 2–3 examples that show problem-solving, teamwork, and ownership.",
            f"Be honest about gaps like {', '.join(missing[:2])}, and explain how you are actively learning them."
        ]

        for tip in tips:
            st.write(f"- {tip}")

        matched_text = "\n".join([f"- {item}" for item in matched])
        missing_text_block = "\n".join([f"- {item}" for item in missing])
        suggestions_text = "\n".join([f"- {item}" for item in suggestions])
        projects_text = "\n".join([f"- {item}" for item in projects])
        improve_lines_text = "\n".join([f"- {item}" for item in improve_lines])
        bullets_text = "\n".join([f"- {item}" for item in bullets])
        tips_text = "\n".join([f"- {item}" for item in tips])

        result_text = f"""AI JOB APPLICATION ASSISTANT RESULT

Match Score: {score}/10

Why this score?
Your resume matches key areas like: {', '.join(matched[:3])}.
Important missing areas: {', '.join(missing[:3])}.

Strengths:
{matched_text}

Missing Skills / Keywords:
{missing_text_block}

Suggestions:
{suggestions_text}

Project Ideas:
{projects_text}

Resume Improvement Lines:
{improve_lines_text}

Tailored Resume Bullet Points:
{bullets_text}

Cover Letter:
{cover_letter}

Interview Tips:
{tips_text}
"""

        st.download_button(
            label="📥 Download Result",
            data=result_text,
            file_name="ai_job_analysis.txt",
            mime="text/plain"
        )

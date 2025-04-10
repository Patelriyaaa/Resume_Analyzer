import streamlit as st
from gemini_utils import analyze_resume_with_gemini
import pdfplumber
import re
import plotly.graph_objects as go

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠")

st.title("🤖 AI-Powered Resume Analyzer")

st.markdown("""
Upload your resume (PDF) and optionally a job description.
Our AI will analyze your resume, compare it with the job, suggest improvements, and visualize your skill match!
""")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description (optional)", height=200)

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skill_data(result_text):
    resume_skills = []
    job_skills = []
    missing_skills = []

    resume_match = re.search(r"Skills in resume:?\n(.*)", result_text, re.IGNORECASE)
    job_match = re.search(r"Skills in job description:?\n(.*)", result_text, re.IGNORECASE)
    missing_match = re.search(r"Missing skills:?\n(.*)", result_text, re.IGNORECASE)

    if resume_match:
        resume_skills = [s.strip() for s in resume_match.group(1).split(",")]
    if job_match:
        job_skills = [s.strip() for s in job_match.group(1).split(",")]
    if missing_match:
        missing_skills = [s.strip() for s in missing_match.group(1).split(",")]

    return resume_skills, job_skills, missing_skills

if uploaded_file:
    with st.spinner("Extracting text and analyzing..."):
        text = extract_text_from_pdf(uploaded_file)
        result = analyze_resume_with_gemini(text, job_description if job_description else None)

    st.success("✅ Analysis Complete!")
    st.markdown("### 📝 Results:")
    st.markdown(result)

    # Extract skills
    resume_skills, job_skills, missing_skills = extract_skill_data(result)

    # Skill Match Chart
    st.markdown("### 📊 Skill Match Breakdown")
    if resume_skills or job_skills or missing_skills:
        data = {
            "Resume Skills": len(resume_skills),
            "Job Description Skills": len(job_skills),
            "Missing Skills": len(missing_skills)
        }

        fig = go.Figure(data=[go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            marker_color=['#4CAF50', '#2196F3', '#F44336']
        )])

        fig.update_layout(title="Skill Match Overview", xaxis_title="Category", yaxis_title="Number of Skills")
        st.plotly_chart(fig)
    else:
        st.info("Could not extract skill data for visualization.")

    # Job Role Suggestions
    job_roles_match = re.search(r"Suggested job roles.*?:\n(.*)", result, re.IGNORECASE)
    if job_roles_match:
        roles = job_roles_match.group(1).split(",")
        st.markdown("### 💼 Suggested Job Titles")
        for role in roles:
            st.write(f"• {role.strip()}")

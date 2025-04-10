import streamlit as st
from resume_utils import extract_text_from_pdf
from gemini_utils import analyze_resume_with_gemini

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🤖 AI-Powered Resume Analyzer")

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

job_description = st.text_area("Paste Job Description (optional)", height=200)

if st.button("Analyze Resume"):
    if uploaded_file:
        with st.spinner("Extracting text and analyzing..."):
            text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume_with_gemini(text, job_description if job_description else None)
        st.success("Analysis Complete!")
        st.markdown("### 📝 Results:")
        st.markdown(result)
    else:
        st.warning("Please upload a resume.")

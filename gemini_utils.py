import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def analyze_resume_with_gemini(text, job_description=None):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    prompt = f"""
    You're an HR expert. Analyze the following resume:
    {text}

    1. One-line summary
    2. Strengths and weaknesses
    3. Skills and gaps
    4. Recommend top 3 online courses
    """

    if job_description:
        prompt += f"\nCompare this resume to the job description:\n{job_description}\n"
        prompt += "5. Match score out of 100\n6. Missing skills\n7. Is it job ready?"

    response = model.generate_content(prompt)
    return response.text

import os
import json
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(
    api_key=api_key
)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an AI Resume Screening Assistant.

Compare the candidate's resume with the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Use exactly this structure:

{{
    "candidate_name": "",
    "match_score": 0,
    "candidate_summary": "",
    "matching_skills": [],
    "missing_skills": [],
    "education": [],
    "experience": [],
    "strengths": [],
    "recommendations": [],
    "justification": ""
}}

Rules:

- match_score must be a number from 0 to 100.
- matching_skills should contain skills from the resume that match the job.
- missing_skills should contain important job requirements missing from the resume.
- education should contain the candidate's educational qualifications.
- experience should contain relevant internships, jobs, and projects.
- strengths should contain the candidate's strongest points for this role.
- recommendations should contain practical suggestions for improving the candidate's suitability.
- justification should briefly explain why the candidate received the match score.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove accidental markdown formatting if Gemini adds it
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    # Convert JSON text into Python dictionary
    result = json.loads(response_text)

    return result


def test_gemini():

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say hello to my Smart Resume Screener project in one sentence."
    )

    return response.text

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from schemas import ScreeningResult

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def screen_resume(job_description: str, resume_text: str) -> ScreeningResult:
    prompt = f"""
You are an expert technical recruiter and hiring manager in 2026.

Analyse the resume against the job description below and return ONLY a JSON object.
No markdown, no explanation — raw JSON only.

JSON format:
{{
  "score": <integer 0-100>,
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "gaps": ["<gap 1>", "<gap 2>"],
  "summary": "<one or two sentence overall verdict>"
}}

Scoring guide:
- 90-100: Near-perfect fit
- 70-89:  Strong candidate, minor gaps
- 50-69:  Decent match, notable gaps
- 30-49:  Weak match, significant gaps
- 0-29:   Poor fit

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip accidental markdown fences if Gemini adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return ScreeningResult(**data)
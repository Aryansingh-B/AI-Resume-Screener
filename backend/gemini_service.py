import os
import json
import re
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from schemas import ScreeningResult

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
logging.error(f"API KEY LOADED: {api_key[:10] if api_key else 'NOT FOUND'}")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def screen_resume(job_description: str, resume_text: str) -> ScreeningResult:
    prompt = f"""
You are an expert technical recruiter in 2026.
Analyse the resume against the job description and return ONLY a JSON object.
No markdown, no explanation — raw JSON only.

JSON format:
{{
  "score": <integer 0-100>,
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "gaps": ["<gap 1>", "<gap 2>"],
  "summary": "<one or two sentence overall verdict>"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        logging.error(f"RAW GEMINI: {raw[:500]}")

        raw = re.sub(r"```(?:json)?", "", raw).strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            raw = match.group(0)

        data = json.loads(raw)
        return ScreeningResult(**data)

    except Exception as e:
        logging.error(f"GEMINI ERROR: {str(e)}")
        raise
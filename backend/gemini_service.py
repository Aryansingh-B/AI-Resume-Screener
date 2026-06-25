import json
import os
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

logger.info(f"✓ API KEY LOADED: {API_KEY[:10]}...")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def screen_resume(job_description: str, resume_text: str) -> dict:
    """Screen a resume against a job description using Gemini API."""
    prompt = f"""Analyze this resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY valid JSON (no markdown):
{{
    "score": <integer 0-100>,
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "gaps": ["gap 1", "gap 2", "gap 3"],
    "summary": "<1-2 sentence assessment>"
}}"""

    try:
        logger.info("Calling Gemini API...")
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        result = json.loads(response_text.strip())
        logger.info(f"✓ Resume screened. Score: {result['score']}")
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parse failed: {e}")
        return {
            "score": 0,
            "strengths": ["Parse error"],
            "gaps": ["API response format error"],
            "summary": "Error processing resume."
        }
    except Exception as e:
        logger.error(f"❌ API error: {e}")
        return {
            "score": 0,
            "strengths": ["API Error"],
            "gaps": ["Failed to reach Gemini API"],
            "summary": f"Error: {str(e)}"
        }
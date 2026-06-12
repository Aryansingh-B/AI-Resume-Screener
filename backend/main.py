from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text_from_pdf
from gemini_service import screen_resume
from schemas import ScreeningResult
import logging

app = FastAPI(
    title="AI Resume Screener",
    description="GenAI-powered resume screening using Google Gemini",
    version="1.0.0"
)

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Resume Screener API is running ✅"}

@app.post("/screen-resume", response_model=ScreeningResult)
async def screen_resume_endpoint(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        logging.error(f"REQUEST RECEIVED - file: {resume.filename}, content_type: {resume.content_type}")
        
        if resume.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

        pdf_bytes = await resume.read()
        logging.error(f"PDF READ: {len(pdf_bytes)} bytes")
        
        resume_text = extract_text_from_pdf(pdf_bytes)
        logging.error(f"TEXT EXTRACTED: {len(resume_text)} chars")

        if not resume_text:
            raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

        result = screen_resume(job_description, resume_text)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"ENDPOINT ERROR: {str(e)}")
        raise
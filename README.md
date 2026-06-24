# AI Resume Screener

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Deployed-2496ED?logo=docker&logoColor=white)

Upload a resume (PDF) + job description → Get an AI-powered match score with key strengths, gaps, and actionable feedback.

---

## Live Demo

- **Frontend:** [Streamlit App](https://ai-resume-screener-pkfk2an7hcpyiqkvujuefn.streamlit.app/)
- **API Docs:** [FastAPI Swagger](https://ai-resume-screener-production-2564.up.railway.app/docs)
- **Code:** [GitHub Repo](https://github.com/Aryansingh-B/AI-Resume-Screener)

---

## What I Built

A GenAI pipeline that:
1. Extracts text from PDF resumes
2. Sends resume + job description to Google Gemini
3. Returns structured JSON with a match score (0-100) + analysis
4. Exposes it as a REST API (FastAPI)
5. Built a user-friendly web interface (Streamlit)
6. Deployed with Docker

**Why this matters:** This project shows I can take an AI model from concept → API → production deployment.

---

## Tech Stack

- **AI:** Google Gemini 2.5 Flash (prompt engineering for structured output)
- **Backend:** FastAPI + Pydantic (type-safe API design)
- **Frontend:** Streamlit (rapid prototyping)
- **PDF Parsing:** PyMuPDF (text extraction)
- **Deployment:** Docker + Railway (backend) + Streamlit Cloud (frontend)

---

## Quick Start

### Requirements
- Python 3.11+
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### Setup

1. **Clone & setup:**
```bash
git clone https://github.com/aryansinghbais/ai-resume-screener.git
cd ai-resume-screener
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r backend/requirements.txt && pip install streamlit requests
```

2. **Add your API key:**
Create `backend/.env`:
```
GEMINI_API_KEY=your_key_here
```

3. **Run locally:**
```bash
# Terminal 1
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2
cd frontend && streamlit run app.py
```

Open http://localhost:8501

### Or use Docker:
```bash
docker-compose up --build
```

---

## How It Works

**Input:**
- Job description (text)
- Resume (PDF file)

**Output:**
```json
{
  "score": 82,
  "strengths": [
    "Strong Python & ML experience",
    "Familiar with data pipelines",
    "Relevant internship background"
  ],
  "gaps": [
    "No cloud platform experience",
    "Limited deployment background"
  ],
  "summary": "Good fit. Recommend for interview."
}
```

**Score guide:**
- 90-100: Near-perfect fit
- 70-89: Strong candidate, minor gaps
- 50-69: Decent match, notable gaps
- <50: Needs development

---

## Project Structure

```
ai-resume-screener/
│
├── backend/                # FastAPI backend
│   ├── main.py             # API entry point
│   ├── gemini_service.py   # LLM integration
│   ├── pdf_utils.py        # PDF parsing
│   ├── schemas.py          # Data validation
│   └── requirements.txt    # Dependencies
│
├──frontend/                # Streamlit frontend
│   ├──app.py               # Web UI
│   └──requirements.txt     # Dependencies
│
├──docker-compose.yml       # Container orchestration
├──Dockerfile               # Backend image
├──.gitignore               # Git exclusions
└──README.md                # Documentation
```

---

## What I Learned

✅ Prompt engineering for structured JSON output from LLMs  
✅ REST API design with FastAPI + type validation  
✅ Real-world data extraction (PDF parsing)  
✅ End-to-end deployment (Docker, Railway, Streamlit Cloud)  
✅ Working with multipart form requests  

---

## Next Steps

Possible improvements:
- Batch screening (multiple resumes at once)
- Score history tracking (database)
- Embedding-based pre-filtering (to reduce API calls)
- Resume parser improvements (handle more formats)

---

## Connect

- **GitHub:** [Aryansingh-B](https://github.com/Aryansingh-B)
- **LinkedIn:** [aryansinghbais8](https://www.linkedin.com/in/aryansinghbais8/)

---

**MIT License** — free to use, fork, and modify.
# 🤖 AI Resume Screener

> A GenAI-powered tool that matches a candidate's resume (PDF) against a job description and returns a structured match score with strengths, gaps, and a summary — built with FastAPI, Google Gemini, Streamlit, and Docker.

---

## 📌 Project Overview

As a data scientist in 2026, knowing how to build and expose AI-powered pipelines is just as important as knowing how to train models. This project demonstrates:

- **Prompt engineering** for structured JSON output from a large language model
- **REST API design** with FastAPI and Pydantic for type-safe request/response models
- **PDF ingestion** — a real-world data extraction task common in DS workflows
- **Streamlit prototyping** for rapid AI tool development
- **Containerisation** with Docker for reproducible, portable deployment

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| AI / LLM | Google Gemini 2.5 Flash API |
| Backend API | FastAPI + Uvicorn |
| PDF Parsing | PyMuPDF (fitz) |
| Data Validation | Pydantic v2 |
| Frontend UI | Streamlit |
| Containerisation | Docker + Docker Compose |
| Language | Python 3.11 |

---

## 📁 Project Structure

```
ai-resume-screener/
│
├── backend/
│   ├── main.py              # FastAPI app — POST /screen-resume endpoint
│   ├── gemini_service.py    # Gemini API integration + prompt engineering
│   ├── schemas.py           # Pydantic request/response models
│   ├── pdf_utils.py         # PDF text extraction using PyMuPDF
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # GEMINI_API_KEY (not committed to git)
│
├── frontend/
│   └── app.py               # Streamlit UI — upload resume, display results
│
├── Dockerfile               # Containerise the FastAPI backend
├── docker-compose.yml       # Orchestrate backend + frontend services
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- A Google Gemini API key → [Get one free at aistudio.google.com](https://aistudio.google.com)
- Docker (optional, for containerised deployment)

### 1. Clone the repository

```bash
git clone https://github.com/aryansinghbais/ai-resume-screener.git
cd ai-resume-screener
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
pip install streamlit requests
```

### 4. Add your API key

Create `backend/.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 Running the Project

### Option A — Local development (two terminals)

**Terminal 1 — Start the FastAPI backend:**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Start the Streamlit frontend:**

```bash
cd frontend
streamlit run app.py
```

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI docs (Swagger) | http://localhost:8000/docs |
| FastAPI docs (ReDoc) | http://localhost:8000/redoc |

### Option B — Docker (one command)

```bash
docker-compose up --build
```

Both services start automatically. Same URLs as above.

---

## 🔌 API Reference

### `POST /screen-resume`

Accepts a job description and a resume PDF, returns a structured match analysis.

**Request** — `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `job_description` | `string` | The full text of the job posting |
| `resume` | `file` (PDF) | The candidate's resume as a PDF |

**Response** — `application/json`

```json
{
  "score": 82,
  "strengths": [
    "Strong Python and ML pipeline experience",
    "Familiarity with SQL and data wrangling",
    "Previous internship in a data-driven role"
  ],
  "gaps": [
    "No experience with cloud platforms (AWS/GCP)",
    "Missing MLOps or model deployment skills"
  ],
  "summary": "Strong junior candidate with solid fundamentals. Would benefit from cloud and deployment experience before stepping into a senior role."
}
```

**Score guide:**

| Score | Meaning |
|---|---|
| 90–100 | Near-perfect fit |
| 70–89 | Strong candidate, minor gaps |
| 50–69 | Decent match, notable gaps |
| 30–49 | Weak match, significant gaps |
| 0–29 | Poor fit |

**Test with curl:**

```bash
curl -X POST http://localhost:8000/screen-resume \
  -F "job_description=We are hiring a Data Scientist with Python, ML, and SQL skills." \
  -F "resume=@/path/to/resume.pdf"
```

---

## 🧠 Prompt Engineering Notes

The core of this project is a structured prompt sent to Gemini that instructs it to return **only a valid JSON object** — no markdown, no preamble. Key decisions:

- The model is given explicit scoring rubrics so scores are consistent across runs
- Output fields (`score`, `strengths`, `gaps`, `summary`) are strictly typed via Pydantic, catching any LLM hallucinations at the API boundary
- Accidental markdown code fences (` ```json `) are stripped before parsing
- The prompt passes the full resume text extracted from PDF, not page-by-page chunks, keeping context coherent for shorter resumes

---

## 🐳 Docker Details

**`Dockerfile`** — builds the FastAPI backend image on `python:3.11-slim`, installs dependencies, and exposes port 8000.

**`docker-compose.yml`** — defines two services:

- `backend` — the FastAPI container, reads `.env` for the API key
- `frontend` — a lightweight Python container that installs Streamlit at runtime and runs `app.py`

The frontend depends on the backend service being healthy before starting.

---

## 🔒 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gemini API key |

Never commit `.env` to version control. The `.gitignore` excludes it by default.

---

## 📦 Dependencies

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
pymupdf==1.24.3
google-generativeai==0.5.4
pydantic==2.7.1
python-dotenv==1.0.1
```

---

## 🗺️ Possible Extensions

- **Batch screening** — accept a ZIP of multiple resumes, return ranked results
- **Score history** — persist results to SQLite or PostgreSQL for tracking over time
- **Bias audit layer** — add a second Gemini call to flag potentially biased language in the job description
- **Embedding similarity** — use sentence embeddings (e.g. `sentence-transformers`) as a pre-filter before the LLM call to reduce API costs
- **Auth** — add API key authentication to the FastAPI endpoint for multi-user deployment

---

## 👤 Author

**Aryan Singh Bais**
GitHub: [github.com/aryansinghbais](https://github.com/Aryansingh-B)
Project: [github.com/aryansinghbais/ai-resume-screener](https://github.com/Aryansingh-B/AI-Resume-Screener)

---

## 📄 License

MIT License — free to use, modify, and distribute.
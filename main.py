
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from PyPDF2 import PdfReader
from io import BytesIO
import importlib.util

# Create FastAPI application
app = FastAPI(
    title="AI Job Application Tracker"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
AI_MATCHER_FILE = BASE_DIR / "ai-matcher.py"

# Load AI matcher module
spec = importlib.util.spec_from_file_location(
    "ai_matcher",
    AI_MATCHER_FILE
)

if spec is None or spec.loader is None:
    raise RuntimeError("AI matcher file could not be loaded")

ai_matcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai_matcher)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# Home page
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# Backend test
@app.get("/api")
def api_home():
    return {
        "message": "AI Job Tracker Backend Connected Successfully!"
    }


# AI Resume Matcher API
@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Check PDF file
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # Check job description
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description."
        )

    try:
        # Read uploaded PDF
        file_content = await resume.read()

        pdf = PdfReader(BytesIO(file_content))

        resume_text = ""

        for page in pdf.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        # Run AI matching
        result = ai_matcher.calculate_match(
            resume_text,
            job_description
        )

        # Career recommendation
        recommendation = ai_matcher.get_recommendation(
            result["match_percentage"]
        )

        return {
            "success": True,
            "filename": resume.filename,
            "match_percentage": result["match_percentage"],
            "skill_match_percentage": result["skill_match_percentage"],
            "text_similarity": result["text_similarity"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "resume_skills": result["resume_skills"],
            "job_skills": result["job_skills"],
            "recommendation": recommendation
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(error)}"
        )

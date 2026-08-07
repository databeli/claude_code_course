import logging

from fastapi import APIRouter, Form, HTTPException, UploadFile

from database import list_analyses, save_analysis
from models import AnalysisSummary, AnalyzeResponse
from services.file_parser import extract_resume_text
from services.gemini_client import analyze_resume

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(
    resume: UploadFile,
    job_description: str = Form(...),
) -> AnalyzeResponse:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    content = await resume.read()
    try:
        resume_text = extract_resume_text(resume.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        result = analyze_resume(resume_text, job_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini API call failed: {exc}") from exc

    try:
        save_analysis(resume.filename, resume_text, job_description, result)
    except Exception:
        logger.exception("Failed to save analysis to the database")

    return AnalyzeResponse(**result)


@router.get("/api/history", response_model=list[AnalysisSummary])
def history_endpoint() -> list[AnalysisSummary]:
    rows = list_analyses()
    return [AnalysisSummary(**dict(row)) for row in rows]

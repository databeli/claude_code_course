from pydantic import BaseModel


class PingGeminiResponse(BaseModel):
    response: str


class AnalyzeResponse(BaseModel):
    score: int
    tier: str
    missing_keywords: list[str]
    skill_gaps: list[str]
    phrasing_suggestions: list[str]


class AnalysisSummary(BaseModel):
    id: int
    created_at: str
    resume_filename: str | None
    job_description: str
    score: int
    tier: str

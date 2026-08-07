from fastapi import APIRouter, HTTPException

from models import PingGeminiResponse
from services.gemini_client import ping_gemini

router = APIRouter()


@router.get("/api/ping-gemini", response_model=PingGeminiResponse)
def ping_gemini_endpoint() -> PingGeminiResponse:
    try:
        text = ping_gemini()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini API call failed: {exc}") from exc
    return PingGeminiResponse(response=text)

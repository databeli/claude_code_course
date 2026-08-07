import json
import os
import re

import google.generativeai as genai

_PING_PROMPT = "Say hello in one short sentence and confirm you are working."

_ANALYZE_PROMPT = """You are a resume screening assistant. Compare the resume below \
against the job description and evaluate how well the candidate fits the role.

Respond with ONLY a JSON object (no markdown fences, no extra text) matching exactly \
this shape:
{{
  "score": <integer 0-100, how well the resume fits the job description>,
  "missing_keywords": [<strings — important JD keywords/skills absent from the resume>],
  "skill_gaps": [<strings — skills or experience the JD requires but the resume lacks>],
  "phrasing_suggestions": [<strings — concrete suggestions to improve resume wording>]
}}

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{jd_text}
\"\"\"
"""

_TIER_THRESHOLDS = (
    (80, "Strong Fit"),
    (60, "Good Fit"),
    (40, "Moderate Fit"),
)
_DEFAULT_TIER = "Weak Fit"


def _tier_for_score(score: int) -> str:
    for threshold, tier in _TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    return _DEFAULT_TIER


def _get_model(model_name: str = "gemini-2.5-flash") -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)


def ping_gemini() -> str:
    model = _get_model()
    result = model.generate_content(_PING_PROMPT)
    return result.text


def analyze_resume(resume_text: str, jd_text: str) -> dict:
    model = _get_model()
    prompt = _ANALYZE_PROMPT.format(resume_text=resume_text, jd_text=jd_text)
    result = model.generate_content(prompt)

    raw = result.text.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned an unexpected (non-JSON) response") from exc

    score = int(data["score"])
    score = max(0, min(100, score))

    return {
        "score": score,
        "tier": _tier_for_score(score),
        "missing_keywords": list(data.get("missing_keywords", [])),
        "skill_gaps": list(data.get("skill_gaps", [])),
        "phrasing_suggestions": list(data.get("phrasing_suggestions", [])),
    }

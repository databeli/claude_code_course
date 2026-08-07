import os
from io import BytesIO

import pdfplumber

ALLOWED_EXTENSIONS = {".pdf", ".md"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def extract_resume_text(filename: str, content: bytes) -> str:
    ext = os.path.splitext(filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Resume must be a .pdf or .md file")

    if len(content) > MAX_FILE_SIZE_BYTES:
        raise ValueError("Resume file exceeds the 10MB size limit")

    if ext == ".md":
        text = content.decode("utf-8", errors="ignore")
    else:
        try:
            with pdfplumber.open(BytesIO(content)) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as exc:
            raise ValueError("Could not read PDF file — it may be corrupt") from exc

    if not text.strip():
        raise ValueError(
            "Resume file appears to be empty — if this is a PDF, it may be a scanned "
            "image with no selectable text"
        )

    return text

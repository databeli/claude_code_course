import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "resume_analyzer.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                resume_filename TEXT,
                resume_text TEXT NOT NULL,
                job_description TEXT NOT NULL,
                score INTEGER NOT NULL,
                tier TEXT NOT NULL,
                recommendations TEXT NOT NULL
            )
            """
        )


def save_analysis(resume_filename: str, resume_text: str, job_description: str, result: dict) -> None:
    recommendations = json.dumps(
        {
            "missing_keywords": result["missing_keywords"],
            "skill_gaps": result["skill_gaps"],
            "phrasing_suggestions": result["phrasing_suggestions"],
        }
    )
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO analyses
                (created_at, resume_filename, resume_text, job_description, score, tier, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                resume_filename,
                resume_text,
                job_description,
                result["score"],
                result["tier"],
                recommendations,
            ),
        )


def list_analyses() -> list[sqlite3.Row]:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, created_at, resume_filename, job_description, score, tier
            FROM analyses
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()

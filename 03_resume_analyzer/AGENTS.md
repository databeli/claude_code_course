# AGENTS.md — Resume Analyzer

## Project Overview

A local full-stack web app where a user uploads a **resume** (PDF or Markdown) and a **job description** (pasted text or file). The app analyzes both using an LLM and returns:
- A **fitment score** (e.g. 0–100, or a labeled tier)
- **Recommendations** (missing keywords, phrasing improvements, skill gaps, formatting notes)

All analysis runs are persisted to a local SQLite database so past uploads/results can be viewed again later.

Specific feature requirements, acceptance criteria, and task scope are tracked in Jira — this file does not duplicate that. It only defines the standing technical conventions the project should follow regardless of which ticket is being worked.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.11+, FastAPI |
| Frontend | React + Vite |
| Database | SQLite (file-based, local) |
| LLM | Gemini API (`google-generativeai` SDK) |
| File parsing | PDF: `pypdf` or `pdfplumber`; Markdown: read as plain text |

---

## Project Structure

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI app entrypoint, CORS, router mounting
│   ├── database.py          # SQLite connection, schema init
│   ├── models.py            # Pydantic request/response schemas
│   ├── routes/
│   │   └── resume.py        # Upload, analyze, fetch history endpoints
│   ├── services/
│   │   ├── gemini_client.py # Gemini API wrapper (prompt building, calls)
│   │   └── file_parser.py   # Extract raw text from PDF/MD uploads
│   ├── requirements.txt
│   └── .env.example         # GEMINI_API_KEY=your_key_here
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   │   └── ResumeReview.jsx
│   │   ├── api/             # fetch wrappers to backend endpoints
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── resume_analyzer.db       # SQLite file (gitignored, created at runtime)
├── .gitignore
└── README.md
```

---

## Database Conventions

- Single SQLite file, created/migrated on app startup via `database.py` — no external migration tool needed for this project's scope.
- Table naming: lowercase, plural (e.g. `analyses`, not `Analysis`).
- Every table includes `id` (primary key), `created_at` (UTC timestamp).
- Store raw extracted resume/JD text alongside the LLM's structured output (score + recommendations as JSON) so past results are fully reproducible without re-calling the LLM.

---

## Backend Conventions

- All endpoints live under `/api/...` and return JSON.
- Use Pydantic models for every request body and response — no raw dicts passed across route boundaries.
- Keep LLM prompt construction inside `services/gemini_client.py`, not inline in route handlers.
- Wrap LLM calls in try/except; on failure, return a clear `502`-style error rather than a silent fallback.
- Environment variables (API keys) loaded via `.env` + `python-dotenv` — never hardcoded, never committed.
- File uploads validated for type (`.pdf`, `.md`) and a reasonable size limit before parsing.

---

## Frontend Conventions

- Functional components with hooks only — no class components.
- Keep API calls in a dedicated `src/api/` module, not scattered inside components.
- Component files use PascalCase; utility/helper files use camelCase.
- Favor small, composable components over large page-level files.

---

## Git & PR Conventions

- Branch naming: `feature/<short-description>` (ticket number can be included if useful, e.g. `feature/jira-123-upload-flow`).
- Commit messages: short imperative summary line (e.g. `Add resume upload endpoint`), body only if extra context is needed.
- One logical change per PR — avoid bundling unrelated fixes.
- PR description should state what changed and how it was tested (manual steps are fine for this project's scope).

---

## Local Development

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

- Backend expected on `http://localhost:8000`, frontend on `http://localhost:5173` (Vite default) — CORS configured accordingly in `main.py`.
- `.env` file required in `backend/` with a valid `GEMINI_API_KEY` before any analysis endpoint will work.

---

## Out of Scope for This File

Feature-level requirements (exact fields shown in the UI, exact scoring rubric, exact recommendation format, etc.) are defined per Jira ticket and should be pulled from there at implementation time — not assumed or hardcoded from this document.

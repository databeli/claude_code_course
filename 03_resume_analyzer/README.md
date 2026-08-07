# Resume Analyzer

Local full-stack app: upload a resume + job description, get an LLM-generated fitment score and recommendations. See [AGENTS.md](AGENTS.md) for tech stack and conventions.

## Current status

Project scaffolding only (KAN-2): FastAPI backend + React (Vite) frontend wired together with a `/api/ping-gemini` smoke-test endpoint to confirm frontend → backend → Gemini works end to end. No resume analysis features yet.

## Running locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in GEMINI_API_KEY
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`. Click "Ping Gemini" to confirm the full stack is wired correctly.

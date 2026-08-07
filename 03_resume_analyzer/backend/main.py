from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from database import init_db  # noqa: E402
from routes.ping import router as ping_router  # noqa: E402
from routes.resume import router as resume_router  # noqa: E402

init_db()

app = FastAPI(title="Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router)
app.include_router(resume_router)

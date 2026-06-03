from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import db

# =========================
# ROUTES
# =========================

from app.routes.auth import router as auth_router
from app.routes.jobs import router as jobs_router
from app.routes.applications import router as applications_router
from app.routes.resume import router as resume_router
from app.routes.voice import router as voice_router
from app.routes.voice_verification import router as voice_verification_router
from app.routes.interview_voice import router as interview_voice_router
from app.routes.questions import router as questions_router
from app.routes.interview import router as interview_router

from app.routes.report import (
    router as report_router
)
# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="RecruitAI Backend",
    version="1.0.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES
# =========================

# AUTH
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# JOBS
app.include_router(
    jobs_router,
    prefix="/jobs",
    tags=["Jobs"]
)

# APPLICATIONS
app.include_router(
    applications_router,
    prefix="/applications",
    tags=["Applications"]
)

# RESUME AI
app.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume AI"]
)

# VOICE SAMPLE
app.include_router(
    voice_router,
    prefix="/voice",
    tags=["Voice Sample"]
)

# VOICE VERIFICATION AI
app.include_router(
    voice_verification_router,
    prefix="/voice-verification",
    tags=["Voice Verification AI"]
)
app.include_router(
    interview_voice_router,
    prefix="/interview-voice",
    tags=["Interview Voice"]
)

app.include_router(
    questions_router,
    prefix="/questions",
    tags=["Questions"]
)

app.include_router(
    interview_router,
    prefix="/interview",
    tags=["Interview"]
)
app.include_router(
    report_router,
    prefix="/report",
    tags=["Report"]
)

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "RecruitAI Backend Running"
    }

# =========================
# TEST DATABASE
# =========================

@app.get("/test-db")
def test_db():

    return {
        "collections": db.list_collection_names()
    }
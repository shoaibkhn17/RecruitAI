from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import pdfplumber

from bson import ObjectId

from app.database.db import db

from app.services.ai_resume_service import (
    extract_skills,
    calculate_match_score
)

router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
async def upload_resume(
    job_id: str = Form(...),
    candidate_email: str = Form(...),
    file: UploadFile = File(...)
):

    print("\n========== RESUME UPLOAD ==========")
    print("JOB ID:", job_id)
    print("EMAIL:", candidate_email)
    print("FILE:", file.filename)
    print("==================================")

    # =========================
    # SAVE PDF
    # =========================

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # =========================
    # EXTRACT PDF TEXT
    # =========================

    extracted_text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    # =========================
    # EXTRACT SKILLS
    # =========================

    resume_skills = extract_skills(
        extracted_text
    )

    # =========================
    # FIND JOB
    # =========================

    job = db.jobs.find_one({
        "_id": ObjectId(job_id)
    })

    if not job:

        return {
            "success": False,
            "error": "Job not found"
        }

    # =========================
    # JOB SKILLS
    # =========================

    job_skills = job.get(
        "skills",
        []
    )

    # =========================
    # CALCULATE MATCH SCORE
    # =========================

    match_result = calculate_match_score(
        resume_skills,
        job_skills
    )

    resume_score = match_result["score"]

    # =========================
    # INTERVIEW ELIGIBILITY
    # =========================

    interview_allowed = (
        resume_score >= 50
    )

    # =========================
    # SAVE APPLICATION
    # =========================

    application_data = {

        "candidate_email":
            candidate_email,

        "job_id":
            job_id,

        "resume_filename":
            file.filename,

        "resume_text":
            extracted_text,

        "resume_skills":
            resume_skills,

        "matched_skills":
            match_result["matched_skills"],

        "missing_skills":
            match_result["missing_skills"],

        "resume_score":
            resume_score,

        "interview_allowed":
            interview_allowed
    }

    print("\n========================")
    print("APPLICATION DATA")
    print("========================")
    print(application_data)

    result = db.applications.insert_one(
        application_data
    )

    print("\nINSERTED ID:")
    print(result.inserted_id)

    print("========================\n")

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "filename":
            file.filename,

        "resume_skills":
            resume_skills,

        "matched_skills":
            match_result["matched_skills"],

        "missing_skills":
            match_result["missing_skills"],

        "resume_score":
            resume_score,

        "interview_allowed":
            interview_allowed,

        "minimum_required_score":
            50,

        "message":
            "Eligible for Interview"
            if interview_allowed
            else
            "Not Eligible for Interview"
    }
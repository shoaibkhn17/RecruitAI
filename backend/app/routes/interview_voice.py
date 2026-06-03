from fastapi import APIRouter, UploadFile, File, Form
import os

from app.database.db import db

from app.services.interview_ai_service import (
    transcribe_audio,
    evaluate_answer
)

router = APIRouter()

INTERVIEW_DIR = "interview_answers"

os.makedirs(
    INTERVIEW_DIR,
    exist_ok=True
)


@router.post("/upload-answer")
async def upload_answer(

    candidate_email: str = Form(...),

    question_number: str = Form(...),

    file: UploadFile = File(...)

):

    safe_email = (
        candidate_email
        .replace("@", "_")
        .replace(".", "_")
    )

    filename = f"{safe_email}_q{question_number}.webm"

    file_path = os.path.join(
        INTERVIEW_DIR,
        filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:

        f.write(contents)

    # =========================
    # AI TRANSCRIPTION
    # =========================

    transcript = transcribe_audio(
        file_path
    )

    evaluation = evaluate_answer(
        transcript
    )

    print("\nTRANSCRIPT:")
    print(transcript)

    print("\nAI SCORE:")
    print(evaluation)

    # =========================
    # SAVE ANSWER IN MONGODB
    # =========================

    db.applications.update_one(

        {
            "candidate_email": candidate_email
        },

        {
            "$push": {
                "interview_answers": {

                    "question_number":
                        question_number,

                    "audio_file":
                        filename,

                    "transcript":
                        transcript,

                    "communication_score":
                        evaluation["communication_score"],

                    "technical_score":
                        evaluation["technical_score"],

                    "overall_score":
                        evaluation["overall_score"]
                }
            }
        }

    )

    return {

        "success": True,

        "file_path": file_path,

        "transcript": transcript,

        "ai_score": evaluation,

        "saved_to_database": True

    }
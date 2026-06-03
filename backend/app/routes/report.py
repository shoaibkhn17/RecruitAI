from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.database.db import db
from app.services.pdf_service import generate_report
from app.services.ml_service import predict_candidate

router = APIRouter()


@router.get("/download-report/{candidate_email}")
def download_report(candidate_email: str):

    safe_email = (
        candidate_email
        .replace("@", "_")
        .replace(".", "_")
    )

    file_path = f"reports/{safe_email}.pdf"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{safe_email}.pdf"
    )


@router.get("/generate-report/{candidate_email}")
def generate_pdf_report(candidate_email: str):

    application = db.applications.find_one(
        {
            "candidate_email": candidate_email
        }
    )

    if not application:

        return {
            "success": False,
            "message": "Application not found"
        }

    answers = application.get(
        "interview_answers",
        []
    )

    scores = []

    for answer in answers:

        score = answer.get(
            "overall_score",
            0
        )

        try:

            scores.append(
                float(score)
            )

        except:

            scores.append(0)

    if len(scores) > 0:

        interview_score = (
            sum(scores) / len(scores)
        )

    else:

        interview_score = 0

    resume_score = application.get(
        "resume_score",
        0
    )

    recommendation = predict_candidate(
        resume_score,
        interview_score
    )

    print("\nAPPLICATION:")
    print(application)

    print("\nANSWERS:")
    print(answers)

    print("\nSCORES:")
    print(scores)

    safe_email = (
        candidate_email
        .replace("@", "_")
        .replace(".", "_")
    )

    pdf_path = generate_report(

        file_path=f"reports/{safe_email}.pdf",

        candidate_email=candidate_email,

        resume_score=resume_score,

        interview_score=round(
            interview_score,
            2
        ),

        recommendation=recommendation
    )

    return {

        "success": True,

        "pdf_path": pdf_path,

        "resume_score": resume_score,

        "interview_score": interview_score,

        "recommendation": recommendation
    }
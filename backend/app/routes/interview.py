from fastapi import APIRouter
from app.database.db import db

router = APIRouter()

@router.post("/complete")

async def complete_interview(data: dict):

    candidate_email = data.get("candidate_email")

    db.applications.update_one(
        {
            "candidate_email": candidate_email
        },
        {
            "$set": {
                "interview_completed": True,
                "voice_verified": True
            }
        }
    )

    return {
        "success": True
    }
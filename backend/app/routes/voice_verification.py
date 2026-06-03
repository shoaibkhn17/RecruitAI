from fastapi import APIRouter
from app.services.voice_verification_service import verify_voice

router = APIRouter()

@router.post("/verify")

async def verify(data: dict):

    original = data.get("original_voice")

    interview = data.get("interview_voice")

    result = verify_voice(
        original,
        interview
    )

    return result
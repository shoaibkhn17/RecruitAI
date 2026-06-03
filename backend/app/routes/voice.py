from fastapi import APIRouter, UploadFile, File, Form
import os

router = APIRouter()

# =========================
# CREATE FOLDER
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VOICE_FOLDER = os.path.join(
    BASE_DIR,
    "../../voice_samples"
)

os.makedirs(VOICE_FOLDER, exist_ok=True)

# =========================
# UPLOAD VOICE
# =========================

@router.post("/upload-voice")
async def upload_voice(

    candidate_email: str = Form(...),

    file: UploadFile = File(...)

):

    try:

        print("UPLOAD STARTED")

        # SAFE FILE NAME
        safe_email = (
            candidate_email
            .replace("@", "_")
            .replace(".", "_")
        )

        file_name = f"{safe_email}.webm"

        file_path = os.path.join(
            VOICE_FOLDER,
            file_name
        )

        # READ FILE
        contents = await file.read()

        print("VOICE SIZE:", len(contents))

        # SAVE FILE
        with open(file_path, "wb") as f:

            f.write(contents)

        print("VOICE SAVED:", file_path)

        return {
            "success": True,
            "message": "Voice uploaded successfully",
            "file_path": file_path
        }

    except Exception as e:

        print("VOICE ERROR:", str(e))

        return {
            "success": False,
            "error": str(e)
        }
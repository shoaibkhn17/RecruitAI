from fastapi import APIRouter
from bson import ObjectId
from app.database.db import db
import random

router = APIRouter()

@router.get("/by-job/{job_id}")
async def get_questions(job_id: str):

    job = db.jobs.find_one({
        "_id": ObjectId(job_id)
    })

    if not job:
        return []

    skills = job.get("skills", [])

    all_questions = []

    for skill in skills:

        docs = list(
            db.questions.find(
                {"category": skill}
            )
        )

        all_questions.extend(docs)

    random.shuffle(all_questions)

    selected = all_questions[:4]

    return [
        {
            "question": q["question"],
            "category": q["category"]
        }
        for q in selected
    ]
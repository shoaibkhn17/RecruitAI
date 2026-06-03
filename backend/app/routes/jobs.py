from fastapi import APIRouter
from app.models.job_model import JobCreate
from app.services.job_service import create_job, get_jobs

router = APIRouter()


@router.post("/create-job")
def add_job(job: JobCreate):

    return create_job(job)


@router.get("/all-jobs")
def all_jobs():

    return get_jobs()
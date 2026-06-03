from fastapi import APIRouter
from app.models.application_model import ApplicationCreate
from app.services.application_service import (
    create_application,
    get_applications
)

router = APIRouter()

@router.post("/apply")
def apply(application: ApplicationCreate):

    return create_application(application)


@router.get("/all")
def all_applications():

    return get_applications()
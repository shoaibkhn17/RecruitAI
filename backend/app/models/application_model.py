from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    name: str
    email: str
    job_id: str
    resume: str
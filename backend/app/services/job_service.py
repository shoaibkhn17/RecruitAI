from app.database.db import db

jobs_collection = db["jobs"]


def create_job(job):

    new_job = {
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "skills": job.skills,
        "experience": job.experience
    }

    result = jobs_collection.insert_one(new_job)

    return {
        "message": "Job created successfully",
        "job_id": str(result.inserted_id)
    }


def get_jobs():

    jobs = []

    for job in jobs_collection.find():

        job["_id"] = str(job["_id"])

        jobs.append(job)

    return jobs
from app.database.db import db

applications_collection = db["applications"]

def create_application(application):

    new_application = {
        "name": application.name,
        "email": application.email,
        "job_id": application.job_id,
        "resume": application.resume
    }

    result = applications_collection.insert_one(new_application)

    return {
        "message": "Application submitted successfully",
        "application_id": str(result.inserted_id)
    }


def get_applications():

    applications = []

    for app in applications_collection.find():

        app["_id"] = str(app["_id"])

        applications.append(app)

    return applications
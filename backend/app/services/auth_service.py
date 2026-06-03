from app.database.db import db
from bcrypt import hashpw, gensalt, checkpw

users_collection = db["users"]


def create_user(user):
    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        return {"error": "User already exists"}

    hashed_password = hashpw(
        user.password.encode('utf-8'),
        gensalt()
    )

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }

    users_collection.insert_one(new_user)

    return {
        "message": "User registered successfully"
    }


def login_user(user):
    existing_user = users_collection.find_one({"email": user.email})

    if not existing_user:
        return {"error": "User not found"}

    password_match = checkpw(
        user.password.encode('utf-8'),
        existing_user["password"]
    )

    if not password_match:
        return {"error": "Invalid password"}

    return {
        "message": "Login successful",
        "user": {
            "name": existing_user["name"],
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    }
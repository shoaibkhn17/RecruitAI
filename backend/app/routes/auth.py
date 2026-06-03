from fastapi import APIRouter
from app.models.user_model import UserRegister, UserLogin
from app.services.auth_service import create_user, login_user

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):
    return create_user(user)


@router.post("/login")
def login(user: UserLogin):
    return login_user(user)
from app.api.actions.auth import AuthService
from app.api.actions.user import UserService


user_service = UserService()
auth_service = AuthService()

def get_user_service():
    return user_service

def get_auth_service():
    return auth_service
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.models.user import User

class AuthController:

    @staticmethod
    def register(user_data: UserCreate, db: Session) -> UserResponse:
        return AuthService.register_user(db, user_data)

    @staticmethod
    def login(login_data: UserLogin, db: Session) -> Token:
        return AuthService.authenticate_user(db, login_data)

    @staticmethod
    def get_me(current_user: User) -> UserResponse:
        return current_user
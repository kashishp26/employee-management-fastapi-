from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.config import get_password_hash, verify_password, create_access_token

class AuthService:

    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        # Check duplicate email
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered"
            )
        
        # Hash password and save
        hashed_pwd = get_password_hash(user_data.password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_pwd,
            role=user_data.role or "USER"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Token:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role, "id": user.id}
        )
        return Token(access_token=access_token, token_type="bearer")
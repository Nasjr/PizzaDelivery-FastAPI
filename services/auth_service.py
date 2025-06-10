from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.hashing_utils import verify_password
from database.models import Order, User
from fastapi import Depends, HTTPException, status
from typing import List

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_email(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    def get_user_name(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    def check_user_exist(self, user: User):
        db_email = self.query(User).filter(User.email == user.email).first()
        db_username = self.query(User).filter(User.name == user.name).first()
        if db_email is not None or db_username is not None:
            raise HTTPException(detail="This user already exists", status_code=status.HTTP_400_BAD_REQUEST)
        return False
    def authenticate_user(self,form_data: OAuth2PasswordRequestForm = Depends()):
        user_db = self.db.query(User).filter(User.name == form_data.username).first()
        if not user_db or not verify_password(form_data.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_db

    def add_new_user(self, new_user: User):
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
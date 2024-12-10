from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import database

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.password != password:  # Простий варіант перевірки пароля
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user

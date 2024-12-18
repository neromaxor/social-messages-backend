from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    telegram_accounts = relationship("TelegramAccount", back_populates="owner")

class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    telegram_id = Column(String, unique=True, index=True)
    session_name = Column(String, nullable=True)  # Add session_name here

    owner = relationship("User", back_populates="telegram_accounts")

# models.py
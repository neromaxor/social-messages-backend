from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class TelegramAccountCreate(BaseModel):
    telegram_id: str  # Замінили int на str для коректного ID Telegram

class TelegramAccount(BaseModel):
    id: int
    telegram_id: str  # Замінили int на str

    class Config:
       from_attributes = True

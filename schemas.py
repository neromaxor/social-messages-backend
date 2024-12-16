from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
       from_attributes = True

class TelegramAccountCreate(BaseModel):
    user_id: int  # ID користувача для підключення акаунта
    telegram_id: str  # Telegram ID

class TelegramAccount(BaseModel):
    id: int
    telegram_id: str

    class Config:
         from_attributes = True

# schemas.py
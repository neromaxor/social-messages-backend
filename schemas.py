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
    telegram_id: str  # Залишимо як string для коректної обробки Telegram ID

class TelegramAccount(BaseModel):
    id: int
    telegram_id: str

    class Config:
        orm_mode = True

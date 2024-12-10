from passlib.context import CryptContext
from telethon.sync import TelegramClient

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_telegram_chats(telegram_id: str):
    with TelegramClient(telegram_id, API_ID, API_HASH) as client:
        dialogs = client.get_dialogs(limit=10)
        return [{"name": dialog.name, "id": dialog.id} for dialog in dialogs]


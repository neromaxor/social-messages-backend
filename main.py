from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database, auth, services
from database import SessionLocal
from config import API_ID, API_HASH
from telethon import TelegramClient  
from schemas import TelegramAccountCreate


app = FastAPI()

# Ініціалізація бази даних
database.init_db()

# Залежність для підключення до БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Кореневий маршрут
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

# Реєстрація користувача
@app.post("/register/", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Хешуємо пароль перед збереженням
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Вхід користувача
@app.post("/login/")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"message": "Logged in successfully"}

# Підключення Telegram акаунта

@app.post("/connect-telegram/")
async def connect_telegram(telegram_account: TelegramAccountCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == telegram_account.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Створення session_name для сесії Telegram
    session_name = f"user_{telegram_account.user_id}_session"
    client = await services.get_telegram_client(session_name, API_ID, API_HASH)

    if not client:
        raise HTTPException(status_code=500, detail="Failed to create Telegram client")

    # Збереження акаунта Telegram в базі даних разом з session_name
    db_telegram_account = models.TelegramAccount(
        user_id=telegram_account.user_id,
        telegram_id=telegram_account.telegram_id,
        phone=telegram_account.phone,
        session_name=session_name  # Збереження session_name в базі даних
    )
    db.add(db_telegram_account)
    db.commit()
    db.refresh(db_telegram_account)

    try:
        # Початкова авторизація через номер телефону
        await services.start_telegram_session(client, telegram_account.phone)

        # Отримання чатів після успішної авторизації
        chats = await services.get_telegram_chats(client)
        await client.disconnect()
        return {"chats": chats}
    except Exception as e:
        await client.disconnect()
        raise HTTPException(status_code=500, detail=f"Error connecting Telegram: {e}")


# Логування користувача в Telegram
@app.post("/logout-telegram/")
async def logout_telegram(user_id: int):
    session_name = f"user_{user_id}_session"
    try:
        client = TelegramClient(session_name, API_ID, API_HASH)
        await client.connect()
        await client.log_out()
        await client.disconnect()
        return {"message": "Logged out successfully"}
    except Exception as e:
        return {"error": str(e)}

# Отримання чатів для конкретного користувача
# services.py
@app.get("/chats/{telegram_id}")
async def get_chats(telegram_id: str, db: Session = Depends(get_db)):
    db_account = db.query(models.TelegramAccount).filter(models.TelegramAccount.telegram_id == telegram_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Telegram account not found")

    try:
        # Отримуємо TelegramClient за session_name
        client = TelegramClient(db_account.session_name, API_ID, API_HASH)
        await client.connect()

        # Отримуємо чати
        chats = await services.get_telegram_chats(client)
        await client.disconnect()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

    return {"chats": chats}







# main.py
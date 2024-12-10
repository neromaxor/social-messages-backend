from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database, auth, services

app = FastAPI()

# Додайте цей метод для кореневого маршруту
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

# Залежність для підключення до БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/login/")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"message": "Logged in successfully"}

@app.post("/connect-telegram/")
async def connect_telegram(telegram_account: schemas.TelegramAccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.TelegramAccount).filter(models.TelegramAccount.telegram_id == telegram_account.telegram_id).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Telegram account already connected")
    
    db_telegram_account = models.TelegramAccount(**telegram_account.dict())
    db.add(db_telegram_account)
    db.commit()
    db.refresh(db_telegram_account)

    try:
        # Отримуємо чати користувача через Telegram API
        chats = services.get_telegram_chats(telegram_account.telegram_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

    return {"chats": chats}

@app.get("/chats/{telegram_id}")
async def get_chats(telegram_id: str, db: Session = Depends(get_db)):
    db_account = db.query(models.TelegramAccount).filter(models.TelegramAccount.telegram_id == telegram_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Telegram account not found")
    
    try:
        # Отримуємо чати користувача через Telegram API
        chats = services.get_telegram_chats(telegram_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

    return {"chats": chats}

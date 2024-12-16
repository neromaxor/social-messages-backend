from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Підключення до бази даних
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Створення engine з параметром check_same_thread=False
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Створення сесії
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()

# Функція для ініціалізації бази даних (створення таблиць)
def init_db():
    import models  # Імпортуємо моделі, щоб вони були доступні для створення таблиць
    Base.metadata.create_all(bind=engine)
# database.py
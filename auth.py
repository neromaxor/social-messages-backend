from passlib.context import CryptContext

# Створюємо контекст для роботи з паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функція для хешування пароля
def hash_password(password: str):
    return pwd_context.hash(password)

# Функція для перевірки пароля
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

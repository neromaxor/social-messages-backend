import sqlite3

# Функція для створення таблиць
def create_tables():
    # Підключення до бази даних
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Створення таблиці для користувачів (якщо її немає)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # Створення таблиці для Telegram акаунтів (якщо її немає)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            telegram_id VARCHAR UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)

    # Підтвердження змін
    conn.commit()

    # Закриття підключення
    conn.close()

    print("Таблиці 'users' та 'telegram_accounts' були створені успішно.")

# Викликаємо функцію для створення таблиць
create_tables()

# init_db.py
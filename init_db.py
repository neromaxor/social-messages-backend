import sqlite3

# Підключення до бази даних (створить файл test.db, якщо його ще немає)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Створення таблиці користувачів (якщо вона не існує)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
""")

# Підтвердження змін
conn.commit()

print("Таблиця 'users' була створена успішно.")

# Закриваємо підключення
conn.close()

import sqlite3

# Підключення до бази даних (якщо файлу test.db немає, він буде створений)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Вивід усіх таблиць у базі даних
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Список таблиць у базі даних:", tables)

conn.close()

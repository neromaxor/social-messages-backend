import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Перевірка наявності таблиць
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Список таблиць:", tables)

# Перевірка вмісту таблиці `users`
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("Користувачі:", users)

conn.close()
# check_tables.py
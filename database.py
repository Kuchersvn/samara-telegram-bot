import sqlite3

# Подключаемся к базе (если её нет — создастся автоматически)
conn = sqlite3.connect('samara_bot.db')
cursor = conn.cursor()

# Создаём таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    photo_path TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    place_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (place_id) REFERENCES places (id)
)
''')

conn.commit()

# --- функции работы с базой ---

def add_place(name, description, photo_path):
    cursor.execute(
        "INSERT INTO places (name, description, photo_path) VALUES (?, ?, ?)",
        (name, description, photo_path)
    )
    conn.commit()

import sqlite3

DB_PATH = 'samara_bot.db'


def get_connection():
    """Создаёт и возвращает новое подключение к базе."""
    conn = sqlite3.connect(DB_PATH)
    return conn


# Создаём таблицы, если их нет
conn = get_connection()
cursor = conn.cursor()

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
    photo_path TEXT,
    latitude REAL,
    longitude REAL
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
conn.close()


# ----------- ФУНКЦИИ ---------------

def add_user(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()


def add_place(name, description, photo_path, latitude=None, longitude=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO places (name, description, photo_path, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
        (name, description, photo_path, latitude, longitude)
    )
    conn.commit()
    conn.close()


def get_places():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM places")
    result = cursor.fetchall()
    conn.close()
    return result


def add_favorite(user_id, place_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favorites (user_id, place_id) VALUES (?, ?)", (user_id, place_id))
    conn.commit()
    conn.close()


def get_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.description
        FROM favorites f
        JOIN places p ON f.place_id = p.id
        WHERE f.user_id = ?
    """, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result

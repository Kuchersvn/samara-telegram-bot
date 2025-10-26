# -*- coding: utf-8 -*-
import sqlite3
import os

DB_PATH = "samara.db"

# ❗ Удаляем старую базу, чтобы избежать дублей
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🧹 Удалена старая база данных samara.db")

# Создаём новую базу
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    description TEXT,
    photo_path TEXT,
    latitude REAL,
    longitude REAL
)
""")

def add_place(name, description, photo_path, latitude=None, longitude=None):
    cursor.execute("""
        INSERT OR IGNORE INTO places (name, description, photo_path, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, photo_path, latitude, longitude))
    conn.commit()

# ---------- ДОСТОПРИМЕЧАТЕЛЬНОСТИ ----------

add_place(
    "Самарская набережная",
    "Самарская набережная — одно из самых популярных и живописных мест города...",
    "photos/naberezhnaya.jpg",
    53.1945, 50.1024
)

add_place(
    "Бункер Сталина",
    "Бункер Сталина — уникальный исторический объект времён Второй мировой войны...",
    "photos/bunker_stalina.jpg",
    53.1966, 50.1005
)

add_place(
    "Монумент 'Ладья'",
    "Монумент 'Ладья' — символ Самары, установленный к 400-летию города...",
    "photos/ladya.jpg",
    53.1865, 50.0911
)

add_place(
    "Площадь Куйбышева",
    "Площадь Куйбышева — центральная площадь Самары и одна из крупнейших в Европе...",
    "photos/kuibyshev_square.jpg",
    53.1959, 50.1021
)

add_place(
    "Жигулёвский пивзавод",
    "Основан в 1881 году. Исторический завод, где варят легендарное 'Жигулёвское' пиво...",
    "photos/zhigulevsky.jpg",
    53.1867, 50.0997
)

add_place(
    "Музей космонавтики им. Королёва",
    "Посвящён истории ракетостроения и освоения космоса...",
    "photos/cosmos_museum.jpg",
    53.2404, 50.2217
)

add_place(
    "Иверский монастырь",
    "Самарский Иверский женский монастырь — один из старейших духовных центров города...",
    "photos/iversky_monastery.jpg",
    53.1888, 50.0745
)

add_place(
    "Парк Гагарина",
    "Парк Гагарина — одно из самых зелёных мест Самары, с аллеями и прудами...",
    "photos/gagarin_park.jpg",
    53.2224, 50.1827
)

print("✅ База данных успешно создана без дублей!")
conn.close()

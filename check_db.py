import sqlite3

conn = sqlite3.connect("samara_bot.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(places)")
for row in cursor.fetchall():
    print(row)

conn.close()

import sqlite3

conn = sqlite3.connect('wellness.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    vata INTEGER,
    pitta INTEGER,
    kapha INTEGER,
    wellness INTEGER,
    dominant_dosha TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")
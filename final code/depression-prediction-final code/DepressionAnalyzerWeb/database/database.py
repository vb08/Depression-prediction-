import sqlite3
import os
DB_NAME = os.path.join(os.path.dirname(__file__), "..", "depression.db")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect(DB_NAME)

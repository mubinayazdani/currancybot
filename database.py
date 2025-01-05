import sqlite3
from datetime import datetime

DB_NAME = "btcn.db"

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA busy_timeout = 3000")  
    return conn

def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                request INTEGER DEFAULT 0,
                joined_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                coin TEXT,
                target_price REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

def add_user(telegram_id, username):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)
        """, (telegram_id, username))
        conn.commit()

def get_user(telegram_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        return cursor.fetchone()

def increment_user_requests(user_id):
    try:
        conn = connect() 
        cursor = conn.cursor()

        cursor.execute("SELECT request FROM users WHERE telegram_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute("UPDATE users SET request = request + 1 WHERE telegram_id = ?", (user_id,))
        else:
            cursor.execute("INSERT INTO users (telegram_id, request) VALUES (?, ?)", (user_id, 1))  
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating request: {e}")

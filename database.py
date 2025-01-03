import sqlite3
from datetime import datetime

DB_NAME = "btnc.db"

def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
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

# def add_alert(user_id, coin, target_price):
#     with connect() as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO alerts (user_id, coin, target_price) VALUES (?, ?, ?)
#         """, (user_id, coin, target_price))
#         conn.commit()

# def get_alerts():
#     with connect() as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT * FROM alerts
#         """)
#         return cursor.fetchall()

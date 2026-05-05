import sqlite3
from datetime import datetime

DB_NAME = "metal.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        copper REAL,
        aluminum REAL
    )
    """)

    conn.commit()
    conn.close()


def save_price(copper, aluminum, date=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    copper_num = float(str(copper).replace(",", ""))
    aluminum_num = float(str(aluminum).replace(",", ""))

    c.execute("""
    INSERT OR REPLACE INTO prices (date, copper, aluminum)
    VALUES (?, ?, ?)
    """, (date, copper_num, aluminum_num))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT date, copper, aluminum
    FROM prices
    ORDER BY date ASC
    """)

    rows = c.fetchall()
    conn.close()
    return rows

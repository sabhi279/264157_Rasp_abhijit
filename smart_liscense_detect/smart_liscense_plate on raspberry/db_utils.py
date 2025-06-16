import sqlite3

def init_db():
    conn = sqlite3.connect("logs/plates.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plate_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plate TEXT,
                    timestamp TEXT,
                    confidence REAL,
                    image_path TEXT
                )''')
    conn.commit()
    conn.close()

def insert_log(plate, timestamp, confidence, image_path):
    conn = sqlite3.connect("logs/plates.db")
    c = conn.cursor()
    c.execute("INSERT INTO plate_logs (plate, timestamp, confidence, image_path) VALUES (?, ?, ?, ?)",
              (plate, timestamp, confidence, image_path))
    conn.commit()
    conn.close()

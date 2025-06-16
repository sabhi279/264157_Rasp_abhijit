# -*- coding: utf-8 -*-
from flask import Flask, jsonify, send_file
import sqlite3
import os

app = Flask(__name__)

# ‚úÖ Compute absolute path to the DB file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../logs/plates.db')

@app.route('/')
def home():
    return "‚úÖ Flask is running and ready."

@app.route('/logs')
def get_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, plate, timestamp, confidence, image_path FROM plate_logs ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        logs = [
            {
                "id": row[0],
                "plate": row[1],
                "timestamp": row[2],
                "confidence": row[3],
                "image_path": row[4]
            } for row in rows
        ]
        return jsonify(logs)
    except Exception as e:
        return f" Error loading logs: {str(e)}", 500


@app.route('/latest-image')
def latest_image():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT image_path FROM plate_logs ORDER BY id DESC LIMIT 1")
        result = c.fetchone()
        conn.close()

        if result:
            rel_path = result[0]
            full_path = os.path.abspath(os.path.join(BASE_DIR, '../', rel_path))
            print(f"DEBUG: Trying to load image: {full_path}")  # Ì†ΩÌ±à Add this line

            if os.path.exists(full_path):
                return send_file(full_path, mimetype='image/jpeg')
            else:
                return f"‚ö†Ô∏è Image file not found at: {full_path}", 404
        else:
            return "‚ö†Ô∏è No image found in database", 404
    except Exception as e:
        return f" Error loading image: {str(e)}", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

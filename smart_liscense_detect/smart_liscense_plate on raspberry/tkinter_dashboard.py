# tkinter_dashboard.py
import tkinter as tk
from tkinter import ttk
import sqlite3
import os

DB_PATH = os.path.join("logs", "plates.db")

def load_data(tree):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, plate, timestamp, confidence FROM plate_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

def main():
    root = tk.Tk()
    root.title("Smart License Plate Logs")
    root.geometry("700x400")

    columns = ("ID", "Plate", "Timestamp", "Confidence")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    load_data(tree)

    root.mainloop()

if __name__ == "__main__":
    main()

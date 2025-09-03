from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
import sqlite3

# file connections
import app

DB_PATH = "todos.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.TodoApp().run()

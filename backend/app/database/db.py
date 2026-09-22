import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "search.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            content TEXT,
            content_hash TEXT,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    
def save_document(url, title, content, content_hash):

    conn = get_connection()

    conn.execute(
        """
        INSERT OR IGNORE INTO documents
        (url, title, content, content_hash)
        VALUES (?, ?, ?, ?)
        """,
        (url, title, content, content_hash)
    )

    conn.commit()
    conn.close()
    
def get_all_documents():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT id, url, title, content
        FROM documents
        """
    ).fetchall()

    conn.close()

    return rows
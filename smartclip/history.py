"""Clipboard history storage backed by SQLite."""

import sqlite3
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "clipboard_history.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            content_type TEXT DEFAULT 'text',
            timestamp REAL NOT NULL,
            pinned INTEGER DEFAULT 0
        )"""
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_timestamp ON history(timestamp DESC)"
    )
    conn.commit()
    return conn


def add_entry(content, content_type="text"):
    conn = get_db()
    conn.execute(
        "INSERT INTO history (content, content_type, timestamp) VALUES (?, ?, ?)",
        (content[:10000], content_type, time.time()),
    )
    conn.commit()
    conn.close()


def get_recent(limit=50):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, content, content_type, timestamp, pinned FROM history ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows


def search_entries(query, limit=50):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, content, content_type, timestamp, pinned FROM history "
        "WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
        (f"%{query}%", limit),
    ).fetchall()
    conn.close()
    return rows


def delete_entry(entry_id):
    conn = get_db()
    conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def pin_entry(entry_id):
    conn = get_db()
    conn.execute(
        "UPDATE history SET pinned = 1 - pinned WHERE id = ?", (entry_id,)
    )
    conn.commit()
    conn.close()


def clear_all():
    conn = get_db()
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def get_count():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    conn.close()
    return count

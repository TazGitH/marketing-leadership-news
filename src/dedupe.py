import hashlib
import os
import sqlite3

from config import DB_PATH


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_items (hash TEXT PRIMARY KEY, link TEXT, title TEXT, created_at TEXT)"
    )
    return conn


def make_hash(title: str, link: str) -> str:
    base = f"{title.strip().lower()}|{link.strip().lower()}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def filter_unseen(items: list[dict]) -> list[dict]:
    conn = _connect()
    cur = conn.cursor()
    unseen = []
    for item in items:
        item_hash = make_hash(item["title"], item["link"])
        cur.execute("SELECT 1 FROM seen_items WHERE hash = ?", (item_hash,))
        if cur.fetchone() is None:
            item["hash"] = item_hash
            unseen.append(item)
    conn.close()
    return unseen


def mark_as_seen(items: list[dict]):
    conn = _connect()
    cur = conn.cursor()
    for item in items:
        cur.execute(
            "INSERT OR IGNORE INTO seen_items (hash, link, title, created_at) VALUES (?, ?, ?, datetime('now'))",
            (item["hash"], item["link"], item["title"]),
        )
    conn.commit()
    conn.close()

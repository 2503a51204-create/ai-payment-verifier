import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)
DATABASE_PATH = DATABASE_DIR / "evidence.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                status TEXT NOT NULL,
                hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def save_result(result):
    init_db()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO evidence
            (file_name, score, status, hash, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                result["file_name"],
                result["score"],
                result["status"],
                result["hash"],
                result["created_at"],
            ),
        )
        connection.commit()


def get_history():
    init_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT file_name, score, status, hash, created_at
            FROM evidence
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()

    return [dict(row) for row in rows]

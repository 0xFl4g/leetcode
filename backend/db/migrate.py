#!/usr/bin/env python3
"""Run database migrations."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "solutions.db"
MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def run_migrations():
    """Run all pending migrations."""
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create migrations tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            applied_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Get applied migrations
    cursor.execute("SELECT name FROM _migrations")
    applied = {row[0] for row in cursor.fetchall()}

    # Find and run pending migrations
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    for migration_file in migration_files:
        name = migration_file.name
        if name in applied:
            print(f"  Skipping {name} (already applied)")
            continue

        print(f"  Running {name}...")
        sql = migration_file.read_text()

        try:
            # Execute migration (may contain multiple statements)
            cursor.executescript(sql)
            cursor.execute("INSERT INTO _migrations (name) VALUES (?)", (name,))
            conn.commit()
            print(f"  ✓ Applied {name}")
        except Exception as e:
            conn.rollback()
            print(f"  ✗ Failed {name}: {e}")
            raise

    conn.close()
    print("Migrations complete!")


if __name__ == "__main__":
    print("Running database migrations...")
    run_migrations()

#!/usr/bin/env python3
"""Demonstrate the restart boundary for memory-only idempotency state."""

from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._keys: set[str] = set()

    def record(self, key: str) -> None:
        self._keys.add(key)

    def exists(self, key: str) -> bool:
        return key in self._keys


class SqliteIdempotencyStore:
    def __init__(self, path: Path) -> None:
        self._connection = sqlite3.connect(path)
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS idempotency_keys (key TEXT PRIMARY KEY)"
        )
        self._connection.commit()

    def record(self, key: str) -> None:
        self._connection.execute(
            "INSERT OR IGNORE INTO idempotency_keys (key) VALUES (?)", (key,)
        )
        self._connection.commit()

    def exists(self, key: str) -> bool:
        row = self._connection.execute(
            "SELECT 1 FROM idempotency_keys WHERE key = ?", (key,)
        ).fetchone()
        return row is not None

    def close(self) -> None:
        self._connection.close()


def main() -> int:
    key = "request-123"

    memory_before_restart = InMemoryIdempotencyStore()
    memory_before_restart.record(key)
    memory_after_restart = InMemoryIdempotencyStore()

    with tempfile.TemporaryDirectory() as tmpdir:
        sqlite_path = Path(tmpdir) / "idempotency.sqlite"
        sqlite_before_restart = SqliteIdempotencyStore(sqlite_path)
        sqlite_before_restart.record(key)
        sqlite_before_restart.close()

        sqlite_after_restart = SqliteIdempotencyStore(sqlite_path)
        memory_survived = memory_after_restart.exists(key)
        sqlite_survived = sqlite_after_restart.exists(key)
        sqlite_after_restart.close()

    print(f"memory_cache_has_key_after_restart={memory_survived}")
    print(f"sqlite_store_has_key_after_restart={sqlite_survived}")

    if memory_survived:
        print("unexpected: in-memory store survived restart")
        return 1
    if not sqlite_survived:
        print("unexpected: sqlite store lost idempotency key")
        return 1

    print("result=in-memory idempotency is restart-local; sqlite persists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

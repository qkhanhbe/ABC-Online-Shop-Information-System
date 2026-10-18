"""DAO layer: one SQLite connection shared by all DAO implementations.

transaction() is how a service makes several DAO calls atomic, e.g. "reserve stock and create
the order" in UC08 step 6: either both are stored or neither (E1 of the specification).
"""
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


class Database:

    def __init__(self, path=":memory:", clock=None):
        self.path = path
        self.conn = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.clock = clock or (lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._depth = 0

    def init_schema(self):
        with open(SCHEMA, encoding="utf-8") as f:
            self.conn.executescript(f.read())
        return self

    def now(self):
        return self.clock()

    @contextmanager
    def transaction(self):
        """Nested calls join the outer transaction; the outermost one commits or rolls back."""
        if self._depth == 0:
            self.conn.execute("BEGIN IMMEDIATE")
        self._depth += 1
        try:
            yield self.conn
        except Exception:
            self._depth -= 1
            if self._depth == 0:
                self.conn.execute("ROLLBACK")
            raise
        else:
            self._depth -= 1
            if self._depth == 0:
                self.conn.execute("COMMIT")

    def execute(self, sql, params=()):
        return self.conn.execute(sql, params)

    def query(self, sql, params=()):
        return self.conn.execute(sql, params).fetchall()

    def query_one(self, sql, params=()):
        return self.conn.execute(sql, params).fetchone()

    def next_id(self, name, prefix, width=3):
        """Human-readable identifiers such as O001, PAY001, EV0001."""
        with self.transaction():
            row = self.query_one("SELECT value FROM sequence WHERE name = ?", (name,))
            value = (row["value"] if row else 0) + 1
            self.execute("INSERT OR REPLACE INTO sequence(name, value) VALUES (?, ?)", (name, value))
        return f"{prefix}{value:0{width}d}"

    def close(self):
        self.conn.close()

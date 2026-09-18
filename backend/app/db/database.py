"""
Phase 7 — Database Setup (SQLite)
Conversational Analytics Platform

Creates the SQLite database file (if it doesn't exist) with the `sales`
table and indexes defined in docs/schema-design.md, and exposes a simple
connection helper for the rest of the backend to use.

Requires: nothing extra — sqlite3 is built into Python.
"""

import sqlite3
import os

# Database file lives alongside this module: backend/app/db/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS sales (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      TEXT    NOT NULL,
    order_date    TEXT    NOT NULL,
    product       TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    city          TEXT    NOT NULL,
    region        TEXT    NOT NULL,
    sales         REAL    NOT NULL,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL    NOT NULL CHECK (unit_price >= 0),
    discount      REAL    NOT NULL,
    profit        REAL    NOT NULL,
    customer_name TEXT    NOT NULL
);
"""

CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_sales_city ON sales (city);",
    "CREATE INDEX IF NOT EXISTS idx_sales_category ON sales (category);",
    "CREATE INDEX IF NOT EXISTS idx_sales_region ON sales (region);",
    "CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales (order_date);",
    "CREATE INDEX IF NOT EXISTS idx_sales_customer_name ON sales (customer_name);",
]


def get_connection() -> sqlite3.Connection:
    """
    Returns a new SQLite connection to the project database.
    row_factory is set so query results behave like dictionaries
    (e.g. row["sales"]) instead of plain tuples.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Creates the sales table and its indexes if they don't already exist."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        for index_sql in CREATE_INDEXES_SQL:
            cursor.execute(index_sql)
        conn.commit()
        print(f"Database ready at: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

    # Quick connection test: insert one dummy row, read it back, then delete it.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sales
            (order_id, order_date, product, category, city, region,
             sales, quantity, unit_price, discount, profit, customer_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("TEST-0001", "2024-01-01", "Test Product", "Test Category",
         "Test City", "Test Region", 100.0, 1, 100.0, 0.0, 20.0, "Test Customer"),
    )
    conn.commit()

    cursor.execute("SELECT * FROM sales WHERE order_id = ?", ("TEST-0001",))
    row = cursor.fetchone()
    print("Test row inserted and read back:", dict(row))

    cursor.execute("DELETE FROM sales WHERE order_id = ?", ("TEST-0001",))
    conn.commit()
    conn.close()

    print("SQLite connection and table verified successfully.")
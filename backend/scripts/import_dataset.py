"""
Phase 8 — Dataset -> Database Import
Conversational Analytics Platform

Reads the cleaned CSV (from Phase 6) and inserts every row into the
SQLite `sales` table (created in Phase 7).

Usage:
    python import_dataset.py

Input:
    dataset/cleaned/sales_cleaned.csv

Output:
    Rows inserted into backend/app/db/database.db -> sales table
"""

import csv
import os
import sys

# Load database.py directly by file path (backend/app/db/database.py).
# This avoids needing __init__.py package files, which are intentionally
# deferred until Phase 9 (Backend Foundation).
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", ".."))
DATABASE_MODULE_PATH = os.path.join(PROJECT_ROOT, "backend", "app", "db", "database.py")

import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("database", DATABASE_MODULE_PATH)
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
get_connection = database.get_connection
init_db = database.init_db

CLEANED_CSV_PATH = os.path.join(PROJECT_ROOT, "dataset", "cleaned", "sales_cleaned.csv")

# Column order in the cleaned CSV must match this exactly (Phase 6 output).
CSV_COLUMNS = [
    "order_id", "order_date", "product", "category", "city", "region",
    "sales", "quantity", "unit_price", "discount", "profit", "customer_name",
]

INSERT_SQL = """
    INSERT INTO sales
        (order_id, order_date, product, category, city, region,
         sales, quantity, unit_price, discount, profit, customer_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def load_rows(csv_path: str):
    """Reads the cleaned CSV and yields tuples ready for INSERT."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Sanity check: make sure the CSV has the columns we expect.
        missing = set(CSV_COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Cleaned CSV is missing expected columns: {missing}")

        for row in reader:
            yield (
                row["order_id"],
                row["order_date"],
                row["product"],
                row["category"],
                row["city"],
                row["region"],
                float(row["sales"]),
                int(row["quantity"]),
                float(row["unit_price"]),
                float(row["discount"]),
                float(row["profit"]),
                row["customer_name"],
            )


def import_dataset(csv_path: str) -> None:
    init_db()  # make sure table + indexes exist before importing

    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Avoid duplicate imports if this script is run more than once.
        cursor.execute("SELECT COUNT(*) FROM sales")
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            print(f"'sales' table already has {existing_count} rows.")
            answer = input("Clear existing data and re-import? (y/n): ").strip().lower()
            if answer == "y":
                cursor.execute("DELETE FROM sales")
                conn.commit()
                print("Existing rows cleared.")
            else:
                print("Import cancelled.")
                return

        rows = list(load_rows(csv_path))
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM sales")
        final_count = cursor.fetchone()[0]
        print(f"Imported {len(rows)} rows. Table 'sales' now has {final_count} rows.")

    finally:
        conn.close()


if __name__ == "__main__":
    if not os.path.exists(CLEANED_CSV_PATH):
        raise FileNotFoundError(
            f"Cleaned dataset not found at: {CLEANED_CSV_PATH}\n"
            "Run backend/scripts/clean_dataset.py first (Phase 6)."
        )
    import_dataset(CLEANED_CSV_PATH)
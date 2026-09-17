"""
Phase 6 — Data Cleaning & Preprocessing
Conversational Analytics Platform

Reads the raw Tableau "Sample - Superstore" Excel file and produces a
cleaned CSV that matches the Phase 3 database schema, ready for
Firestore import in Phase 8.

Usage:
    python clean_dataset.py

Input:
    dataset/raw/sample_-_superstore.xls   (Orders sheet)

Output:
    dataset/cleaned/sales_cleaned.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------
# 1. Paths
# ---------------------------------------------------------------------
RAW_PATH = os.path.join("dataset", "raw", "sample_-_superstore.xls")
CLEANED_DIR = os.path.join("dataset", "cleaned")
CLEANED_PATH = os.path.join(CLEANED_DIR, "sales_cleaned.csv")

# ---------------------------------------------------------------------
# 2. Load raw data (Orders sheet only)
# ---------------------------------------------------------------------
def load_raw_data(path: str) -> pd.DataFrame:
    print(f"Reading raw dataset from: {path}")
    # requires `xlrd` for legacy .xls files -> pip install xlrd
    df = pd.read_excel(path, sheet_name="Orders", engine="xlrd")
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df


# ---------------------------------------------------------------------
# 3. Column mapping (Phase 5 Step 4 — Dataset-to-Schema Mapping)
# ---------------------------------------------------------------------
COLUMN_MAP = {
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Product Name": "product",
    "Category": "category",
    "City": "city",
    "Region": "region",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit",
    "Customer Name": "customer_name",
}

TEXT_FIELDS = ["order_id", "product", "category", "city", "region", "customer_name"]


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # 3a. Keep only the columns we need, rename to schema field names
    df = df[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP)

    # 3b. order_date: string -> proper datetime (Firestore Timestamp on import)
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")

    # 3c. Trim leading/trailing whitespace on text fields
    for col in TEXT_FIELDS:
        df[col] = df[col].astype(str).str.strip()

    # 3d. Derive unit_price = sales / quantity, rounded to 2 decimals
    df["unit_price"] = (df["sales"] / df["quantity"]).round(2)

    # 3e. Round sales/profit/discount to 2 decimals for consistency
    for col in ["sales", "profit", "discount"]:
        df[col] = df[col].round(2)

    # 3f. Reorder columns to match the Phase 3 schema order
    schema_order = [
        "order_id", "order_date", "product", "category", "city", "region",
        "sales", "quantity", "unit_price", "discount", "profit", "customer_name",
    ]
    df = df[schema_order]

    return df


# ---------------------------------------------------------------------
# 4. Validation (sanity checks before saving)
# ---------------------------------------------------------------------
def validate(df: pd.DataFrame) -> None:
    assert df.isnull().sum().sum() == 0, "Cleaned data contains null values!"
    assert (df["quantity"] > 0).all(), "Found non-positive quantity values!"
    assert (df["unit_price"] >= 0).all(), "Found negative unit_price values!"
    assert df["order_id"].str.len().gt(0).all(), "Found empty order_id values!"
    print("Validation passed: no nulls, quantity > 0, unit_price >= 0, order_id non-empty.")


# ---------------------------------------------------------------------
# 5. Save cleaned dataset
# ---------------------------------------------------------------------
def save_cleaned(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned dataset saved to: {path}")
    print(f"Final shape: {df.shape[0]} rows x {df.shape[1]} columns")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
if __name__ == "__main__":
    raw_df = load_raw_data(RAW_PATH)
    cleaned_df = clean_dataset(raw_df)
    validate(cleaned_df)
    save_cleaned(cleaned_df, CLEANED_PATH)
    
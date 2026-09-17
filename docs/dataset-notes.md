# Phase 4 & 5 — Dataset Selection & Understanding

## 4.1 Dataset Source

The platform uses Tableau's official **"Sample - Superstore"** dataset.

- Source: https://public.tableau.com/app/resources/sample-data
- File: `Sample - Superstore.xls`
- Sheets included: `Orders`, `Returns`, `People`
- Only the **`Orders`** sheet is used by this project.

This dataset was chosen over third-party Kaggle re-uploads because it is the
authoritative, original source that most Kaggle "Superstore" datasets are
themselves copied from. Using the original avoids inconsistent or modified
third-party versions.

## 4.2 Known Limitation

The dataset is **US-based** (US cities, states, and regions). It does not
contain Pakistani cities such as Faisalabad or Lahore. This is an accepted
limitation for the initial build — city values are only data, not logic, so
the system's behavior is identical regardless of which country's cities are
in the data. Example/demo questions during development will therefore use
US city names (e.g. "New York", "Houston") instead of Pakistani ones.

---

## 5.1 Dataset Overview

| Metric | Value |
| --- | --- |
| Total rows | 10,194 |
| Unique orders | 5,111 (an order can contain multiple product line items) |
| Total columns (raw) | 21 |
| Date range | 2023-01-03 to 2026-12-30 |
| Missing/null values | 0 |
| Duplicate rows | 0 |

## 5.2 Raw Columns (Orders sheet)

`Row ID`, `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`, `Customer ID`,
`Customer Name`, `Segment`, `Country/Region`, `City`, `State/Province`,
`Postal Code`, `Region`, `Product ID`, `Category`, `Sub-Category`,
`Product Name`, `Sales`, `Quantity`, `Discount`, `Profit`

## 5.3 Categorical Field Breakdown

| Field | Unique Values |
| --- | --- |
| Region | 4 — Central, East, South, West |
| Category | 3 — Office Supplies, Furniture, Technology |
| City | 542 |
| Segment | 3 — Consumer, Home Office, Corporate |

## 5.4 Data Quality Inspection (Step 3) — Result: PASS

- No missing values in any column.
- No duplicate rows.
- 1,901 records have a negative `Profit` value. These are **not data
  errors** — they represent legitimate loss-making transactions (e.g. high
  discounts) and are **retained**, not removed.

## 5.5 Dataset-to-Schema Mapping (Step 4) — Result: COMPLETE

11 of the 12 required schema fields map directly to a dataset column.
`unit_price` has no direct source column and is derived.

| Schema Field | Source Column | Notes |
| --- | --- | --- |
| `order_id` | `Order ID` | Direct |
| `order_date` | `Order Date` | Direct (parsed from string to datetime) |
| `product` | `Product Name` | Direct — **not** `Product ID` |
| `category` | `Category` | Direct |
| `city` | `City` | Direct |
| `region` | `Region` | Direct |
| `sales` | `Sales` | Direct |
| `quantity` | `Quantity` | Direct |
| `unit_price` | *(derived)* | `unit_price = Sales ÷ Quantity` (post-discount effective price) |
| `discount` | `Discount` | Direct |
| `profit` | `Profit` | Direct |
| `customer_name` | `Customer Name` | Direct |

### Columns Dropped (not part of the schema)

`Row ID`, `Ship Date`, `Ship Mode`, `Customer ID`, `Segment`,
`Country/Region`, `State/Province`, `Postal Code`, `Product ID`,
`Sub-Category`

## 5.6 Overall Assessment

The dataset is well-suited for this project: it is clean (no nulls or
duplicates), an appropriate size for development and testing, and has
enough categorical and geographic variety (3 categories, 4 regions, 542
cities) to meaningfully exercise all 17 approved use cases from Phase 2.

## 5.7 Phase 4 & 5 Acceptance Criteria

- [x] Dataset source selected and justified.
- [x] Known limitations documented (US-only geography).
- [x] Full dataset inspected (row count, columns, nulls, duplicates).
- [x] Categorical fields profiled.
- [x] Every schema field mapped to a source column or derivation rule.
- [x] Unmapped/extra columns identified for exclusion.

**Phase 4 & 5 Status: COMPLETE**
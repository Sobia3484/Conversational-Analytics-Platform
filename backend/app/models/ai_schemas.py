"""
Phase 10 — AI Engine (Gemini)
Pydantic model describing the structured JSON that Gemini must return
after interpreting a user's natural-language question.

This schema is deliberately generic enough to cover all 17 approved
Phase 2 use cases:
  - aggregate: total/avg sales, profit, quantity (optionally grouped)
  - lookup: raw record retrieval (e.g. a customer's orders)
  - correlation: two numeric metrics plotted against each other (scatter)
"""

from pydantic import BaseModel
from typing import Optional, Literal, List


class QueryFilters(BaseModel):
    # A list so a question naming specific values (e.g. "compare Furniture
    # and Technology") can filter to exactly those, instead of falling
    # back to a full breakdown of every category/region. A single-value
    # question (e.g. "sales in the West region") is just a list of one.
    category: Optional[List[str]] = None   # e.g. ["Office Supplies"], ["Furniture", "Technology"]
    city: Optional[str] = None
    region: Optional[List[str]] = None     # e.g. ["East"], ["East", "West"]
    customer_name: Optional[str] = None
    start_date: Optional[str] = None     # "YYYY-MM-DD"
    end_date: Optional[str] = None       # "YYYY-MM-DD"


class QueryParams(BaseModel):
    # False if the question is outside this platform's scope (per
    # docs/requirements.md Section 9 — not weather/medical/coding/etc).
    is_supported: bool

    # "aggregate" -> SUM/COUNT/AVG with optional GROUP BY
    # "lookup"    -> raw matching rows (e.g. customer order history)
    # "correlation" -> two numeric fields plotted against each other
    query_type: Optional[Literal["aggregate", "lookup", "correlation"]] = None

    metric: Optional[Literal["sales", "profit", "quantity"]] = None
    aggregation: Optional[Literal["sum", "count", "average"]] = None
    group_by: Optional[Literal["category", "region", "city", "product", "month", "none"]] = "none"

    filters: QueryFilters = QueryFilters()

    order: Optional[Literal["asc", "desc"]] = None
    limit: Optional[int] = None

    # Only used when query_type == "correlation" (e.g. sales vs profit)
    correlation_metric: Optional[Literal["sales", "profit", "quantity", "unit_price"]] = None

    chart_type: Optional[Literal["kpi", "bar", "line", "table", "scatter"]] = None

    # Set when is_supported is False, to explain why (shown to the user).
    rejection_reason: Optional[str] = None
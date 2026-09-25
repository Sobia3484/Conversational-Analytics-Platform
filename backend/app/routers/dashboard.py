"""
Phase 17 addition — Dashboard endpoint
Conversational Analytics Platform

Returns a fixed bundle of KPIs and chart-ready breakdowns for a given
date range. This deliberately skips the AI engine entirely — the
parameters (start_date/end_date) are already structured, so there is
nothing for an LLM to interpret. This makes the Dashboard page instant,
reliable (no dependency on 9 separate AI calls all succeeding), and free
of any AI API usage.
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.ai_schemas import QueryParams, QueryFilters
from app.services.query_engine import run_query

router = APIRouter()


def _aggregate(metric, group_by=None, filters=None, order=None, limit=None):
    params = QueryParams(
        is_supported=True,
        query_type="aggregate",
        metric=metric,
        aggregation="sum",
        group_by=group_by,
        filters=filters or QueryFilters(),
        order=order,
        limit=limit,
    )
    return run_query(params)


def _single_value(rows):
    if rows and rows[0].get("value") is not None:
        v = rows[0]["value"]
        return round(v, 2) if isinstance(v, float) else v
    return 0


@router.get("/dashboard")
def get_dashboard(
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    recent_limit: int = Query(10, description="How many of the latest orders to include"),
):
    """
    GET /dashboard
    GET /dashboard?start_date=2025-01-01&end_date=2025-03-31
    GET /dashboard?recent_limit=25
    """
    filters = QueryFilters(start_date=start_date, end_date=end_date)

    total_sales = _single_value(_aggregate("sales", filters=filters))
    total_profit = _single_value(_aggregate("profit", filters=filters))
    total_quantity = _single_value(_aggregate("quantity", filters=filters))

    category_breakdown = _aggregate("sales", group_by=["category"], filters=filters)
    region_breakdown = _aggregate("sales", group_by=["region"], filters=filters)
    monthly_trend = _aggregate("sales", group_by=["month"], filters=filters)
    top_products = _aggregate("sales", group_by=["product"], filters=filters,
                               order="desc", limit=5)

    correlation_params = QueryParams(
        is_supported=True, query_type="correlation",
        metric="sales", correlation_metric="profit", filters=filters,
    )
    correlation = run_query(correlation_params)

    # "Recent orders" = the most recently dated rows in the (optionally
    # filtered) data — not a real-world "last 7 days", since this demo
    # dataset's dates don't track the actual calendar.
    recent_params = QueryParams(
        is_supported=True, query_type="lookup", filters=filters, limit=recent_limit,
    )
    recent_orders = run_query(recent_params)  # query_engine already orders by order_date DESC

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_quantity": total_quantity,
        "category_breakdown": category_breakdown,
        "region_breakdown": region_breakdown,
        "monthly_trend": monthly_trend,
        "top_products": top_products,
        "correlation": correlation,
        "recent_orders": recent_orders,
    }
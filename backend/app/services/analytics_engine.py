"""
Phase 13 — Analytics Engine
Conversational Analytics Platform

Takes the raw rows from the Query Engine (Phase 12) plus the original
QueryParams (Phase 10/11), and shapes them into the final response format
the frontend expects — matching docs/requirements.md's component mapping:
    aggregate_data  -> KPI card (single number)
    category_data   -> Bar/Pie chart (grouped by category/region/city/product)
    trend_data      -> Line chart (grouped by month)
    correlation_data -> Scatter plot
    list_query      -> Data table (raw records)

Also enforces the Phase 1 requirement: never invent data. If the query
returned no rows (or a null aggregate), the response says "No data found
for the requested criteria" instead of fabricating a number.
"""

from app.models.ai_schemas import QueryParams
from app.models.schemas import QueryResponse

NO_DATA_MESSAGE = "No data found for the requested criteria."


def _round_numeric(value):
    """Rounds floats to 2 decimals for clean display; leaves other types as-is."""
    if isinstance(value, float):
        return round(value, 2)
    return value


def _round_row(row: dict) -> dict:
    return {k: _round_numeric(v) for k, v in row.items()}


def build_response(params: QueryParams, rows: list[dict]) -> QueryResponse:
    """
    Shapes `rows` (from query_engine.run_query) into the final
    QueryResponse the API will send to the frontend.
    """
    # --- No data at all: never invent a number, say so plainly ---
    if not rows:
        return QueryResponse(response_type="list_query", data=[], message=NO_DATA_MESSAGE)

    rows = [_round_row(r) for r in rows]

    # --- Lookup: raw records -> table ---
    if params.query_type == "lookup":
        return QueryResponse(response_type="list_query", data=rows)

    # --- Correlation: x/y pairs -> scatter plot ---
    if params.query_type == "correlation":
        return QueryResponse(response_type="correlation_data", data=rows)

    # --- Aggregate: shape depends on whether/how it was grouped ---
    if params.query_type == "aggregate":
        group_dims = list(params.group_by or [])

        # Ungrouped aggregate (e.g. "total sales") -> single KPI value
        if not group_dims:
            value = rows[0].get("value")
            if value is None:
                return QueryResponse(response_type="aggregate_data", data=None, message=NO_DATA_MESSAGE)
            return QueryResponse(response_type="aggregate_data", data={"value": value})

        # "month" involved (alone or combined with another dimension) ->
        # time trend -> line chart. When combined (e.g. month+category),
        # each row also carries a "series_label" for a multi-line chart.
        if "month" in group_dims:
            return QueryResponse(response_type="trend_data", data=rows)

        # Grouped by category/region/city/product (no time dimension) ->
        # comparison -> bar/pie chart
        return QueryResponse(response_type="category_data", data=rows)

    # Should not happen if Phase 11 validation ran first, but fail safely
    # rather than guessing a shape.
    return QueryResponse(
        response_type="list_query", data=rows,
        message="Unrecognized query type; showing raw results.",
    )


if __name__ == "__main__":
    from app.models.ai_schemas import QueryFilters
    from app.services.query_engine import run_query

    test_cases = [
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=None, chart_type="kpi"),
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["category"], chart_type="bar"),
        QueryParams(is_supported=True, query_type="lookup",
                    filters=QueryFilters(customer_name="Darren Powers"),
                    limit=3, chart_type="table"),
        # Deliberately impossible filter -> should trigger "no data" path
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=None,
                    filters=QueryFilters(city="Atlantis"), chart_type="kpi"),
        # New: 2-dimension grouping (category sales trend over time)
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["month", "category"], chart_type="line"),
    ]

    for i, tc in enumerate(test_cases, 1):
        rows = run_query(tc)
        response = build_response(tc, rows)
        print(f"\n--- Test {i} ---")
        print(response.model_dump_json(indent=2))
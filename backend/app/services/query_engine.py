"""
Phase 12 — Query Engine
Conversational Analytics Platform

Takes a validated QueryParams object (Phase 10 + 11) and builds/executes
the corresponding parameterized SQL query against the SQLite `sales`
table, returning plain Python dicts ready for the Analytics Engine
(Phase 13) and the frontend charts (Phase 17).

All user-influenced values (filter values, dates) are passed as bound
parameters ("?"), never string-interpolated — this prevents SQL
injection. Only fixed, schema-validated tokens (column names, ASC/DESC,
aggregation functions) are ever interpolated directly into the SQL text.
"""

from app.db.database import get_connection
from app.models.ai_schemas import QueryParams, QueryFilters

# Fixed, whitelisted mappings — never derived from raw user input, so it's
# safe to interpolate these into SQL text directly.
METRIC_COLUMN = {
    "sales": "sales",
    "profit": "profit",
    "quantity": "quantity",
    "unit_price": "unit_price",
}

AGG_FUNC = {
    "sum": "SUM",
    "count": "COUNT",
    "average": "AVG",
}

GROUP_BY_COLUMN = {
    "category": "category",
    "region": "region",
    "city": "city",
    "product": "product",
    "month": "strftime('%Y-%m', order_date)",
}


def _build_where_clause(filters: QueryFilters):
    """Returns (sql_fragment, bound_params) for the WHERE clause."""
    clauses = []
    values = []

    if filters.category:
        placeholders = ", ".join("?" for _ in filters.category)
        clauses.append(f"category IN ({placeholders})")
        values.extend(filters.category)
    if filters.city:
        clauses.append("city LIKE ?")
        values.append(f"%{filters.city}%")
    if filters.region:
        placeholders = ", ".join("?" for _ in filters.region)
        clauses.append(f"region IN ({placeholders})")
        values.extend(filters.region)
    if filters.customer_name:
        clauses.append("customer_name LIKE ?")
        values.append(f"%{filters.customer_name}%")
    if filters.start_date:
        clauses.append("order_date >= ?")
        values.append(filters.start_date)
    if filters.end_date:
        clauses.append("order_date <= ?")
        values.append(filters.end_date)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return where_sql, values


def _run_aggregate(cursor, params: QueryParams) -> list[dict]:
    metric_col = METRIC_COLUMN[params.metric]
    agg_func = AGG_FUNC[params.aggregation or "sum"]
    where_sql, where_values = _build_where_clause(params.filters)

    group_dims = list(params.group_by or [])
    # If "month" is one of the dimensions, put it first so it naturally
    # reads as group_label (x-axis / time), with the other dimension (if
    # any) as series_label — matching how a "trend by X" chart is drawn.
    group_dims.sort(key=lambda g: 0 if g == "month" else 1)
    group_cols = [GROUP_BY_COLUMN[g] for g in group_dims]

    if not group_cols:
        sql = f"SELECT {agg_func}({metric_col}) AS value FROM sales {where_sql}"
        cursor.execute(sql, where_values)
        return [dict(row) for row in cursor.fetchall()]

    if len(group_cols) == 1:
        select_cols = f"{group_cols[0]} AS group_label"
        group_by_sql = group_cols[0]
    else:
        # Exactly 2 dimensions supported (e.g. month + category).
        select_cols = f"{group_cols[0]} AS group_label, {group_cols[1]} AS series_label"
        group_by_sql = f"{group_cols[0]}, {group_cols[1]}"

    sql = f"SELECT {select_cols}, {agg_func}({metric_col}) AS value FROM sales {where_sql} GROUP BY {group_by_sql}"

    if "month" in group_dims:
        # A trend/time chart must always read chronologically — sorting by
        # value here would scramble the timeline, so ignore params.order
        # (which is meant for rankings, not time series) and sort by the
        # month itself instead. strftime('%Y-%m', ...) sorts correctly as
        # plain text since it's zero-padded (e.g. "2025-03" < "2025-11").
        sql += " ORDER BY group_label ASC"
    elif params.order:
        sql += f" ORDER BY value {params.order.upper()}"

    if params.limit:
        sql += f" LIMIT {int(params.limit)}"

    cursor.execute(sql, where_values)
    return [dict(row) for row in cursor.fetchall()]


def _run_lookup(cursor, params: QueryParams) -> list[dict]:
    where_sql, where_values = _build_where_clause(params.filters)
    sql = f"SELECT * FROM sales {where_sql} ORDER BY order_date DESC"
    if params.limit:
        sql += f" LIMIT {int(params.limit)}"
    cursor.execute(sql, where_values)
    return [dict(row) for row in cursor.fetchall()]


def _run_correlation(cursor, params: QueryParams) -> list[dict]:
    x_col = METRIC_COLUMN[params.metric]
    y_col = METRIC_COLUMN[params.correlation_metric]
    where_sql, where_values = _build_where_clause(params.filters)
    sql = f"SELECT {x_col} AS x, {y_col} AS y FROM sales {where_sql}"
    cursor.execute(sql, where_values)
    return [dict(row) for row in cursor.fetchall()]


def run_query(params: QueryParams) -> list[dict]:
    """
    Executes the query described by `params` (already validated by
    Phase 11) and returns a list of row dicts.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params.query_type == "aggregate":
            return _run_aggregate(cursor, params)
        elif params.query_type == "lookup":
            return _run_lookup(cursor, params)
        elif params.query_type == "correlation":
            return _run_correlation(cursor, params)
        else:
            raise ValueError(f"Unsupported query_type: {params.query_type}")
    finally:
        conn.close()


if __name__ == "__main__":
    import json

    test_cases = [
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=None, chart_type="kpi"),
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["product"], order="desc",
                    limit=5, chart_type="bar"),
        QueryParams(is_supported=True, query_type="lookup",
                    filters=QueryFilters(customer_name="Darren Powers"),
                    limit=5, chart_type="table"),
        QueryParams(is_supported=True, query_type="correlation", metric="sales",
                    correlation_metric="profit", chart_type="scatter"),
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["category"],
                    filters=QueryFilters(region=["West"]), chart_type="bar"),
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["category"],
                    filters=QueryFilters(category=["Furniture", "Technology"]),
                    chart_type="bar"),
        # New: 2-dimension grouping (category sales trend over time)
        QueryParams(is_supported=True, query_type="aggregate", metric="sales",
                    aggregation="sum", group_by=["month", "category"],
                    chart_type="line"),
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {tc.query_type} (metric={tc.metric}, group_by={tc.group_by}) ---")
        result = run_query(tc)
        print(json.dumps(result[:5], indent=2))  # print first 5 rows only
        print(f"({len(result)} total row(s))")
        
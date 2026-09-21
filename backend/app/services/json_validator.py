"""
Phase 11 — AI JSON Validation
Conversational Analytics Platform

Gemini's structured output (Phase 10) already passes basic type validation
via Pydantic (QueryParams). This layer adds BUSINESS-LOGIC validation that
Pydantic types alone can't catch:
  - category/region values must exactly match what's actually in the data
    (normalizes case, e.g. "technology" -> "Technology")
  - date filters must be valid YYYY-MM-DD and start_date <= end_date
  - the combination of query_type/metric/correlation_metric must be
    internally consistent
  - limit must be a positive number

Raises ValidationError with a clear, user-facing message on failure, so
the API layer (Phase 14) can catch it and respond gracefully instead of
crashing or silently running a bad query.
"""

from datetime import datetime
from app.models.ai_schemas import QueryParams

# Canonical values actually present in the dataset (Phase 5 findings).
# Keys are lowercase for case-insensitive matching; values are the exact
# strings stored in the database.
VALID_CATEGORIES = {
    "office supplies": "Office Supplies",
    "furniture": "Furniture",
    "technology": "Technology",
}
VALID_REGIONS = {
    "central": "Central",
    "east": "East",
    "south": "South",
    "west": "West",
}


class ValidationError(Exception):
    """Raised when Gemini's output fails business-logic validation."""
    pass


def _validate_date(value: str, field_name: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(
            f"'{field_name}' must be a valid date in YYYY-MM-DD format, got '{value}'."
        )


def validate_query_params(params: QueryParams) -> QueryParams:
    """
    Validates and normalizes a QueryParams object. Returns the (possibly
    normalized) object if valid, or raises ValidationError if not.
    """
    # If the AI already flagged this as out-of-scope, nothing else to check —
    # the caller should just surface params.rejection_reason to the user.
    if not params.is_supported:
        return params

    errors = []
    filters = params.filters

    # --- Normalize + validate category (now a list) ---
    if filters.category:
        normalized = []
        for cat in filters.category:
            key = cat.strip().lower()
            if key not in VALID_CATEGORIES:
                errors.append(
                    f"Unknown category '{cat}'. "
                    f"Valid categories: {', '.join(VALID_CATEGORIES.values())}."
                )
            else:
                normalized.append(VALID_CATEGORIES[key])
        filters.category = normalized

    # --- Normalize + validate region (now a list) ---
    if filters.region:
        normalized = []
        for reg in filters.region:
            key = reg.strip().lower()
            if key not in VALID_REGIONS:
                errors.append(
                    f"Unknown region '{reg}'. "
                    f"Valid regions: {', '.join(VALID_REGIONS.values())}."
                )
            else:
                normalized.append(VALID_REGIONS[key])
        filters.region = normalized

    # --- Validate dates ---
    if filters.start_date:
        try:
            _validate_date(filters.start_date, "start_date")
        except ValidationError as e:
            errors.append(str(e))
    if filters.end_date:
        try:
            _validate_date(filters.end_date, "end_date")
        except ValidationError as e:
            errors.append(str(e))
    if filters.start_date and filters.end_date and not errors:
        if filters.start_date > filters.end_date:
            errors.append("'start_date' cannot be after 'end_date'.")

    # --- query_type-specific consistency checks ---
    if params.query_type == "aggregate":
        if not params.metric:
            errors.append("An aggregate query must specify a metric (sales, profit, or quantity).")
    elif params.query_type == "correlation":
        if not params.metric or not params.correlation_metric:
            errors.append("A correlation query must specify both metric and correlation_metric.")
        elif params.metric == params.correlation_metric:
            errors.append("correlation_metric must be different from metric.")
    elif params.query_type == "lookup":
        pass  # no filters required — a lookup with no filters just lists all records
    else:
        errors.append("query_type is missing or invalid even though is_supported is true.")

    # --- Limit sanity check ---
    if params.limit is not None and params.limit <= 0:
        errors.append("'limit' must be a positive number.")

    if errors:
        raise ValidationError(" ".join(errors))

    return params


if __name__ == "__main__":
    from app.models.ai_schemas import QueryFilters

    print("--- Valid case ---")
    valid = QueryParams(
        is_supported=True, query_type="aggregate", metric="sales",
        aggregation="sum", group_by="category",
        filters=QueryFilters(category=["technology"]),  # lowercase on purpose
        chart_type="bar",
    )
    result = validate_query_params(valid)
    print("Normalized category:", result.filters.category)  # should be ["Technology"]

    print("\n--- Invalid category ---")
    try:
        bad_category = QueryParams(
            is_supported=True, query_type="aggregate", metric="sales",
            filters=QueryFilters(category=["Electronics"]), chart_type="bar",
        )
        validate_query_params(bad_category)
    except ValidationError as e:
        print("Caught as expected:", e)

    print("\n--- Invalid date range ---")
    try:
        bad_dates = QueryParams(
            is_supported=True, query_type="aggregate", metric="sales",
            filters=QueryFilters(start_date="2024-12-31", end_date="2024-01-01"),
            chart_type="kpi",
        )
        validate_query_params(bad_dates)
    except ValidationError as e:
        print("Caught as expected:", e)

    print("\n--- Correlation with same metric twice ---")
    try:
        bad_corr = QueryParams(
            is_supported=True, query_type="correlation", metric="sales",
            correlation_metric="sales", chart_type="scatter",
        )
        validate_query_params(bad_corr)
    except ValidationError as e:
        print("Caught as expected:", e)
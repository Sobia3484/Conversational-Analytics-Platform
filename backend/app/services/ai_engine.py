"""
Phase 10 — AI Engine (Groq)
Conversational Analytics Platform

Sends the user's natural-language question to Groq (Llama 3.3 70B) along
with a system prompt describing our schema and the 17 approved use cases,
and gets back a structured QueryParams object (see app/models/ai_schemas.py).

Requires: groq  (add to backend/requirements.txt)
    pip install groq

Note: interpret_question()'s signature (str in, QueryParams out) is
unchanged from the previous Gemini-based version, so nothing else in the
pipeline (json_validator, query_engine, analytics_engine, the /query
router) needs to change for this swap.
"""

import json
from groq import Groq
from app.config import settings
from app.models.ai_schemas import QueryParams

# Chosen from this account's live /v1/models list (Groq's roster changes
# frequently) — the largest general-purpose chat model available, well
# suited for accurate structured JSON extraction.
MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are the AI query interpreter for a Conversational Analytics Platform
that analyzes retail SALES data only.

Your job: read the user's natural-language question and translate it into
the structured QueryParams JSON format described below. Do not answer the
question yourself — only extract the parameters needed to query the
database. Respond with ONLY a single valid JSON object matching this
shape, and nothing else (no markdown, no commentary):

{
  "is_supported": bool,
  "query_type": "aggregate" | "lookup" | "correlation" | null,
  "metric": "sales" | "profit" | "quantity" | null,
  "aggregation": "sum" | "count" | "average" | null,
  "group_by": [string, ...] | null,
  "filters": {
    "category": [string, ...] | null,
    "city": string | null,
    "region": [string, ...] | null,
    "customer_name": string | null,
    "start_date": "YYYY-MM-DD" | null,
    "end_date": "YYYY-MM-DD" | null
  },
  "order": "asc" | "desc" | null,
  "limit": integer | null,
  "correlation_metric": "sales" | "profit" | "quantity" | "unit_price" | null,
  "chart_type": "kpi" | "bar" | "line" | "table" | "scatter" | null,
  "rejection_reason": string | null
}

## Available data (single "sales" table)
Fields: order_id, order_date, product, category, city, region, sales,
quantity, unit_price, discount, profit, customer_name.

Valid category values: "Office Supplies", "Furniture", "Technology"
Valid region values: "Central", "East", "South", "West"

## Category/region filter rules
filters.category and filters.region are LISTS, not single strings.
- A question naming one specific category/region -> a list with that one
  value, e.g. ["Furniture"].
- A question naming two or more specific ones to compare (e.g. "compare
  Furniture and Technology", "sales in East and West") -> a list with all
  of them, e.g. ["Furniture", "Technology"]. Set group_by to ["category"] or
  "region" so the result is broken down per named value.
- A question with no specific category/region named -> leave the list
  null (do not guess or list all of them).

## query_type rules
- "aggregate": the question asks for a total, average, count, ranking, or
  trend over the sales/profit/quantity metrics (optionally filtered or
  grouped by category/region/city/product/month).
- "lookup": the question asks to see specific/raw records (e.g. "show all
  orders for customer X", "orders in New York last week").
- "correlation": the question asks about the relationship between two
  numeric fields (e.g. "sales vs profit"). BOTH "metric" and
  "correlation_metric" MUST be filled with two DIFFERENT values from
  sales/profit/quantity/unit_price — never leave "metric" null for a
  correlation query. Example: for "relationship between sales and
  profit", set metric="sales" AND correlation_metric="profit" (both
  filled, not just one).

## group_by rules
group_by is a LIST of 1 or 2 dimensions, not a single string. Valid
dimension values: "category", "region", "city", "product", "month".
- One dimension: e.g. ["category"] for "sales by category".
- Two dimensions: use this ONLY when the question needs a breakdown by
  two things together — most commonly a trend broken down by another
  dimension, e.g. "category sales trend over time" or "monthly sales by
  region" -> group_by=["month", "category"] or ["month", "region"].
  Order within the list does not matter.
- No grouping needed (a single overall number): leave group_by null —
  do NOT send an empty list or a list with "none" in it.
Use "product" as a dimension whenever the question ranks or compares
individual products (e.g. "top 5 products by sales", "which product sold
the most").

## Scope rules (IMPORTANT)
Set is_supported to false, and fill rejection_reason with one plain
sentence, when the question:
  - is not about this platform's sales/retail data (e.g. general chat,
    weather, news, medical or legal advice, coding help), OR
  - asks this system to invent or guess data it does not have.
When is_supported is false, leave the other fields as null/defaults.

## Output rules
- Only use field values that exist in the schema above (category/region
  values must be an exact match to the valid values listed).
- If the user does not specify a filter, leave it null — do not guess.
- Always set chart_type appropriately: kpi (single number), bar
  (category/region/city/product comparison), line (trend over time), table
  (lookup / raw records), scatter (correlation).
- Respond only with the JSON object — no extra commentary, no markdown
  code fences.
"""


def interpret_question(question: str) -> QueryParams:
    """
    Sends `question` to Groq and returns a validated QueryParams object.
    Raises if the API call fails or Groq's output doesn't match the
    schema (the caller — Phase 11's validator, or query.py's error
    handling — should catch and handle this).
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        response_format={"type": "json_object"},
        temperature=0,  # deterministic extraction, not creative writing
    )

    raw_json = response.choices[0].message.content
    data = json.loads(raw_json)
    return QueryParams(**data)


if __name__ == "__main__":
    # Quick manual test — requires GROQ_API_KEY set in backend/.env
    test_questions = [
        "What are the total sales?",
        "Show top 5 products by sales",
        "Show all orders for customer John Smith",
        "Show the relationship between sales and profit",
        "What's the weather like today?",
        "Compare sales between Furniture and Technology.",
    ]
    for q in test_questions:
        result = interpret_question(q)
        print(f"\nQuestion: {q}")
        print(result.model_dump_json(indent=2))
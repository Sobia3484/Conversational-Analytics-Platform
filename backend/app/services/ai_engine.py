"""
Phase 10 — AI Engine (Gemini)
Conversational Analytics Platform

Sends the user's natural-language question to Gemini along with a system
prompt describing our schema and the 17 approved use cases, and gets back
a structured QueryParams object (see app/models/ai_schemas.py).

Requires: google-genai  (add to backend/requirements.txt)
    pip install google-genai
"""

from google import genai
from app.config import settings
from app.models.ai_schemas import QueryParams

# Model choice: gemini-2.5-flash is fast and inexpensive, well suited for
# this kind of short structured-extraction task.
MODEL_NAME = "gemini-3.6-flash"

SYSTEM_PROMPT = """
You are the AI query interpreter for a Conversational Analytics Platform
that analyzes retail SALES data only.

Your job: read the user's natural-language question and translate it into
the structured QueryParams JSON format you have been given as your
response schema. Do not answer the question yourself — only extract the
parameters needed to query the database.

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
  of them, e.g. ["Furniture", "Technology"]. Set group_by to "category" or
  "region" so the result is broken down per named value.
- A question with no specific category/region named -> leave the list
  null (do not guess or list all of them).

## query_type rules
- "aggregate": the question asks for a total, average, count, ranking, or
  trend over the sales/profit/quantity metrics (optionally filtered or
  grouped by category/region/city/month).
- "lookup": the question asks to see specific/raw records (e.g. "show all
  orders for customer X", "orders in New York last week").
- "correlation": the question asks about the relationship between two
  numeric fields (e.g. "sales vs profit").

## group_by rules
Valid group_by values: "category", "region", "city", "product", "month", "none".
Use "product" whenever the question ranks or compares individual products
(e.g. "top 5 products by sales", "which product sold the most").

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
  (category/region/city comparison), line (trend over time), table
  (lookup / raw records), scatter (correlation).
- Respond only with the structured JSON — no extra commentary.
"""


def interpret_question(question: str) -> QueryParams:
    """
    Sends `question` to Gemini and returns a validated QueryParams object.
    Raises if the API call fails or Gemini's output doesn't match the schema
    (the caller — Phase 11's validator — should catch and handle this).
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_schema": QueryParams,
        },
    )

    # response.parsed is already a validated QueryParams instance when
    # response_schema is a Pydantic model (google-genai handles this).
    return response.parsed


if __name__ == "__main__":
    # Quick manual test — requires GEMINI_API_KEY set in backend/.env
    test_questions = [
        "What are the total sales?",
        "Show top 5 products by sales",
        "Show all orders for customer John Smith",
        "Show the relationship between sales and profit",
        "What's the weather like today?",
    ]
    for q in test_questions:
        result = interpret_question(q)
        print(f"\nQuestion: {q}")
        print(result.model_dump_json(indent=2))
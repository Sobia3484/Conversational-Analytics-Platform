"""
Phase 14 — Backend API Complete
The real /query endpoint, wiring together the full pipeline:

    user question
        -> ai_engine.interpret_question()      (Phase 10 — Gemini)
        -> json_validator.validate_query_params() (Phase 11)
        -> query_engine.run_query()            (Phase 12 — SQLite)
        -> analytics_engine.build_response()   (Phase 13 — shape for frontend)
        -> QueryResponse back to the caller
"""

from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.ai_engine import interpret_question
from app.services.json_validator import validate_query_params, ValidationError
from app.services.query_engine import run_query
from app.services.analytics_engine import build_response

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest) -> QueryResponse:
    # Step 1: Ask Gemini to interpret the natural-language question.
    try:
        params = interpret_question(request.question)
    except Exception:
        # Phase 18 will add more specific error handling/logging here.
        return QueryResponse(
            response_type="list_query",
            data=[],
            message="Sorry, I couldn't process that question right now. Please try again.",
        )

    # Step 2: If the question is out of this platform's scope, say so —
    # per docs/requirements.md, this is not a general-purpose assistant.
    if not params.is_supported:
        return QueryResponse(
            response_type="list_query",
            data=[],
            message=params.rejection_reason or "This question is outside what this platform can answer.",
        )

    # Step 3: Business-logic validation (categories/regions/dates/consistency).
    try:
        params = validate_query_params(params)
    except ValidationError as e:
        return QueryResponse(
            response_type="list_query",
            data=[],
            message=f"I couldn't understand part of that question: {e}",
        )

    # Step 4: Run the SQL query against the database.
    rows = run_query(params)

    # Step 5: Shape the result for the frontend (or "no data" message).
    return build_response(params, rows)
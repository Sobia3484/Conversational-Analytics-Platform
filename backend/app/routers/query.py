"""
Phase 9 — Backend Foundation
The /query endpoint. Currently a placeholder — Phase 10 will replace the
body with a real call to the Gemini AI engine, Phase 12 will add the real
SQL query engine, and Phase 13 the analytics engine.
"""

from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest) -> QueryResponse:
    """
    Placeholder implementation so the API structure can be tested end to
    end before the AI engine (Phase 10) and query engine (Phase 12) exist.
    """
    return QueryResponse(
        response_type="aggregate_data",
        data={"placeholder": True, "received_question": request.question},
        message="This is a placeholder response. AI engine (Phase 10) and "
                "query engine (Phase 12) are not implemented yet.",
    )

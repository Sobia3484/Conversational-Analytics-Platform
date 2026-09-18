"""
Phase 9 — Backend Foundation
Pydantic models for request/response validation on the /query endpoint.
"""

from pydantic import BaseModel
from typing import Any, List, Optional


class QueryRequest(BaseModel):
    """What the frontend sends when the user asks a question."""
    question: str


class QueryResponse(BaseModel):
    """
    What the backend sends back. `response_type` tells the frontend which
    component to render (see docs/requirements.md component mapping):
    sales_data, trend_data, category_data, correlation_data, list_query,
    aggregate_data.
    """
    response_type: str
    data: Any
    message: Optional[str] = None

"""
Phase 9 — Backend Foundation
FastAPI application entrypoint. Mounts the query router and enables CORS
so the React frontend (Phase 15+) can call this API from a different port.

Run with (from the backend/ folder):
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for the interactive Swagger UI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import query, dashboard
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

# Allow the frontend (running on a different port during development) to
# call this API. Tighten allow_origins to the real frontend URL in Phase 20
# (Security & Code Cleanup) before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME}
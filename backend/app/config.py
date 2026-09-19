"""
Phase 9 — Backend Foundation
Loads environment variables (e.g. GEMINI_API_KEY, added in Phase 10) from
backend/.env so the rest of the app can read them via `settings`.

Requires: python-dotenv (add to backend/requirements.txt)
"""

import os
from dotenv import load_dotenv

# Load backend/.env regardless of the current working directory
# (this file is at backend/app/config.py, so two levels up is backend/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    APP_NAME: str = "Conversational Analytics Platform"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
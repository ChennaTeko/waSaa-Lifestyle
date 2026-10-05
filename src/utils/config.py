"""Central place for paths, constants and settings."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

RAW_SERVICES = RAW_DIR / "services_raw.csv"
RAW_QUERIES = RAW_DIR / "queries_seed.csv"

CLEANED = PROCESSED_DIR / "services_cleaned.csv"
VALIDATED = PROCESSED_DIR / "services_validated.csv"
REJECTED = PROCESSED_DIR / "rejected_rows.csv"
NLP_READY = PROCESSED_DIR / "nlp_ready.csv"
REPORT = PROCESSED_DIR / "pipeline_report.json"

CATEGORIES = [
    "Healthcare", "Transport", "Beauty & Wellness",
    "Domestic Services", "Education Support",
]
AREAS = [
    "Westlands", "Kilimani", "Lavington", "Karen", "Kileleshwa", "Parklands",
    "CBD", "South B", "Kasarani", "Ruaka", "Embakasi", "Rongai",
]
CITY = "Nairobi"
CURRENCY = "KES"
DATA_ORIGINS = ["public", "synthetic", "hybrid"]
MIN_DESCRIPTION_WORDS = 10


def database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Copy .env.example to .env first.")
    return url

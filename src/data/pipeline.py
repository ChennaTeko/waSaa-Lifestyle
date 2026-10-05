"""Runs RAW -> CLEANED -> VALIDATED -> NLP-READY. Usage: python -m src.data.pipeline"""
import json

import pandas as pd

from src.data.cleaning import clean
from src.data.validation import validate
from src.nlp.text import build_nlp_text
from src.utils import config


def run() -> dict:
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(config.RAW_SERVICES, dtype=str, keep_default_na=False)
    cleaned = clean(raw)
    cleaned.to_csv(config.CLEANED, index=False)

    valid, rejected = validate(cleaned)
    valid.insert(0, "service_id", range(1, len(valid) + 1))
    valid.to_csv(config.VALIDATED, index=False)
    rejected.to_csv(config.REJECTED, index=False)

    nlp = valid[["service_id", "service_name", "category", "area"]].copy()
    nlp["nlp_text"] = build_nlp_text(valid)
    nlp.to_csv(config.NLP_READY, index=False)

    report = {
        "raw_rows": len(raw),
        "cleaned_rows": len(cleaned),
        "valid_rows": len(valid),
        "rejected_rows": len(rejected),
        "rows_by_category": valid["category"].value_counts().to_dict(),
        "rows_by_data_origin": valid["data_origin"].value_counts().to_dict(),
    }
    config.REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    for key, value in run().items():
        print(f"{key}: {value}")

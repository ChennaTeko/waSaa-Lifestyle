"""STAGE 1: RAW -> CLEANED. Fixes formatting only; does not judge correctness."""
import re

import pandas as pd

from src.utils.config import AREAS, CATEGORIES

TEXT_COLS = ["provider_name", "service_name", "category", "description",
             "keywords", "area", "city", "availability_days", "data_origin"]
NUM_COLS = ["price_min", "price_max", "rating_avg", "review_count"]

_CATEGORY_LOOKUP = {c.lower(): c for c in CATEGORIES}
_CATEGORY_LOOKUP.update({"beauty and wellness": "Beauty & Wellness",
                         "beauty": "Beauty & Wellness"})
_AREA_LOOKUP = {a.lower(): a for a in AREAS}


def _squash(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in TEXT_COLS:
        out[col] = out[col].map(_squash)
    out["category"] = out["category"].map(lambda v: _CATEGORY_LOOKUP.get(v.lower(), v))
    out["area"] = out["area"].map(lambda v: _AREA_LOOKUP.get(v.lower(), v))
    out["keywords"] = out["keywords"].str.lower().str.replace(r"\s*,\s*", ", ", regex=True)
    out["data_origin"] = out["data_origin"].str.lower()
    for col in NUM_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce")  # bad values -> NaN, never 0
    return out

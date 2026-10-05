"""STAGE 2: CLEANED -> VALIDATED. Applies the integrity rules from docs/data_requirements.md."""
import pandas as pd

from src.utils.config import AREAS, CATEGORIES, DATA_ORIGINS, MIN_DESCRIPTION_WORDS

REQUIRED = ["provider_name", "service_name", "category", "description", "area", "data_origin"]


def row_problems(row: pd.Series) -> list:
    problems = []
    for col in REQUIRED:
        if not str(row[col]).strip():
            problems.append(f"missing {col}")
    if row["category"] and row["category"] not in CATEGORIES:
        problems.append("unknown category")
    if row["area"] and row["area"] not in AREAS:
        problems.append("unknown area")
    if row["data_origin"] and row["data_origin"] not in DATA_ORIGINS:
        problems.append("invalid data_origin")
    if len(str(row["description"]).split()) < MIN_DESCRIPTION_WORDS and row["description"]:
        problems.append(f"description shorter than {MIN_DESCRIPTION_WORDS} words")
    pmin, pmax = row["price_min"], row["price_max"]
    if pd.notna(pmin) and pmin < 0:
        problems.append("negative price_min")
    if pd.notna(pmax) and pmax < 0:
        problems.append("negative price_max")
    if pd.notna(pmin) and pd.notna(pmax) and pmin > pmax:
        problems.append("price_min greater than price_max")
    if pd.notna(row["rating_avg"]) and not 0 <= row["rating_avg"] <= 5:
        problems.append("rating outside 0-5")
    if pd.notna(row["review_count"]) and row["review_count"] < 0:
        problems.append("negative review_count")
    return problems


def validate(df: pd.DataFrame):
    """Return (valid_df, rejected_df). Rejected rows carry a 'reject_reason' column."""
    df = df.reset_index(drop=True)
    reasons = [row_problems(row) for _, row in df.iterrows()]

    seen, dup = set(), []
    for _, row in df.iterrows():
        key = (row["provider_name"].lower(), row["service_name"].lower())
        dup.append(key in seen)
        seen.add(key)
    for i, is_dup in enumerate(dup):
        if is_dup:
            reasons[i].append("duplicate (provider_name, service_name)")

    bad = pd.Series([bool(r) for r in reasons])
    rejected = df[bad].copy()
    rejected["reject_reason"] = ["; ".join(r) for r in reasons if r]
    valid = df[~bad].copy().reset_index(drop=True)
    return valid, rejected

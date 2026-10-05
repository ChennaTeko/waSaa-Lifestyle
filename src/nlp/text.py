"""Builds the NLP text field. Rule: location, price and rating are NOT part of nlp_text."""
import re

import pandas as pd


def normalise_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_nlp_text(df: pd.DataFrame) -> pd.Series:
    combined = (df["service_name"] + " " + df["category"] + " "
                + df["description"] + " " + df["keywords"].fillna(""))
    return combined.map(normalise_text)

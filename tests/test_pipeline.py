import pandas as pd

from src.data import pipeline
from src.nlp.text import build_nlp_text, normalise_text
from src.utils import config


def test_normalise_text():
    assert normalise_text("  Hair, Braids!! ") == "hair braids"


def test_pipeline_end_to_end():
    report = pipeline.run()
    assert report["raw_rows"] == report["valid_rows"] + report["rejected_rows"]
    assert report["rejected_rows"] >= 1          # the deliberately dirty rows
    assert set(report["rows_by_category"]) == set(config.CATEGORIES)

    nlp = pd.read_csv(config.NLP_READY)
    assert nlp["nlp_text"].notna().all() and (nlp["nlp_text"].str.len() > 0).all()


def test_nlp_text_excludes_price_and_location():
    df = pd.read_csv(config.VALIDATED, keep_default_na=False)
    text = build_nlp_text(df)
    # the Kasarani painter has an area but nlp_text must never contain area names or price numbers
    row = df[df["service_name"] == "House painting"].index[0]
    assert "kasarani" not in text[row]
    assert "4 0" not in text[row]

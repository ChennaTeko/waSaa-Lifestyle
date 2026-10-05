import pandas as pd

from src.data.cleaning import clean


def _row(**kw):
    base = dict(provider_name="P", service_name="S", category="Healthcare",
                description="word " * 12, keywords="a,b", area="Karen", city="Nairobi",
                price_min="100", price_max="200", rating_avg="4.5", review_count="10",
                availability_days="Daily", data_origin="synthetic")
    base.update(kw)
    return pd.DataFrame([base])


def test_whitespace_collapsed():
    assert clean(_row(provider_name="  Glow   Salon "))["provider_name"][0] == "Glow Salon"


def test_category_and_area_normalised():
    out = clean(_row(category="beauty", area="westlands"))
    assert out["category"][0] == "Beauty & Wellness"
    assert out["area"][0] == "Westlands"


def test_bad_number_becomes_nan_not_zero():
    out = clean(_row(price_min="abc", price_max=""))
    assert pd.isna(out["price_min"][0]) and pd.isna(out["price_max"][0])


def test_data_origin_lowercased():
    assert clean(_row(data_origin="SYNTHETIC"))["data_origin"][0] == "synthetic"

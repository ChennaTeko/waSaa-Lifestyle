import pandas as pd

from src.data.cleaning import clean
from src.data.validation import validate


def _df(**kw):
    base = dict(provider_name="P", service_name="S", category="Healthcare",
                description="word " * 12, keywords="a, b", area="Karen", city="Nairobi",
                price_min="100", price_max="200", rating_avg="4.5", review_count="10",
                availability_days="Daily", data_origin="synthetic")
    base.update(kw)
    return clean(pd.DataFrame([base]))


def test_good_row_passes():
    valid, rejected = validate(_df())
    assert len(valid) == 1 and len(rejected) == 0


def test_price_min_greater_than_max_rejected():
    _, rejected = validate(_df(price_min="500", price_max="100"))
    assert "price_min greater than price_max" in rejected["reject_reason"].iloc[0]


def test_rating_out_of_range_rejected():
    valid, rejected = validate(_df(rating_avg="7.2"))
    assert len(valid) == 0 and len(rejected) == 1


def test_short_description_rejected():
    valid, _ = validate(_df(description="too short"))
    assert len(valid) == 0


def test_unknown_area_rejected():
    valid, _ = validate(_df(area="Atlantis"))
    assert len(valid) == 0


def test_missing_price_is_allowed():
    valid, _ = validate(_df(price_min="", price_max=""))
    assert len(valid) == 1


def test_duplicate_rejected():
    two = pd.concat([_df(), _df()], ignore_index=True)
    valid, rejected = validate(two)
    assert len(valid) == 1 and len(rejected) == 1

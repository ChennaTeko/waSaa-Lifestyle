"""Loads VALIDATED data into PostgreSQL. Usage: python -m src.database.load
Re-runnable: it recreates the schema every time."""
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from src.nlp.text import build_nlp_text
from src.utils import config

SCHEMA = config.ROOT / "database" / "schema.sql"


def _none(v):
    return None if pd.isna(v) else v


def load() -> dict:
    df = pd.read_csv(config.VALIDATED, keep_default_na=False, na_values=[""])
    df["keywords"] = df["keywords"].fillna("")
    df["nlp_text"] = build_nlp_text(df)
    queries = pd.read_csv(config.RAW_QUERIES, keep_default_na=False)

    conn = psycopg2.connect(config.database_url())
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SCHEMA.read_text(encoding="utf-8"))

            execute_values(cur, "INSERT INTO categories (category_name) VALUES %s",
                           [(c,) for c in config.CATEGORIES])
            execute_values(cur, "INSERT INTO locations (city, area) VALUES %s",
                           [(config.CITY, a) for a in sorted(df["area"].unique())])

            cur.execute("SELECT category_name, category_id FROM categories")
            cat_id = dict(cur.fetchall())
            cur.execute("SELECT area, location_id FROM locations")
            loc_id = dict(cur.fetchall())

            # one provider row per (name, area); rating = mean across its rows
            prov = (df.groupby(["provider_name", "area"], as_index=False)
                      .agg(rating_avg=("rating_avg", "mean"),
                           review_count=("review_count", "max"),
                           data_origin=("data_origin", "first")))
            execute_values(cur, """INSERT INTO providers
                (provider_name, location_id, rating_avg, review_count, data_origin) VALUES %s""",
                [(r.provider_name, loc_id[r.area],
                  None if pd.isna(r.rating_avg) else round(float(r.rating_avg), 1),
                  None if pd.isna(r.review_count) else int(r.review_count),
                  r.data_origin) for r in prov.itertuples()])
            cur.execute("""SELECT p.provider_name, l.area, p.provider_id
                           FROM providers p JOIN locations l USING (location_id)""")
            prov_id = {(n, a): i for n, a, i in cur.fetchall()}

            execute_values(cur, """INSERT INTO services
                (service_id, provider_id, category_id, service_name, description, keywords,
                 price_min, price_max, availability_days, nlp_text, data_origin) VALUES %s""",
                [(int(r.service_id), prov_id[(r.provider_name, r.area)], cat_id[r.category],
                  r.service_name, r.description, r.keywords,
                  _none(r.price_min), _none(r.price_max), _none(r.availability_days),
                  r.nlp_text, r.data_origin) for r in df.itertuples()])

            execute_values(cur, """INSERT INTO service_requests
                (query_text, query_type, target_category, location_constraint,
                 budget_max, language, created_by) VALUES %s""",
                [(q.query_text, q.query_type, q.target_category or None,
                  q.location_constraint or None,
                  float(q.budget_max) if str(q.budget_max).strip() else None,
                  q.language, q.created_by) for q in queries.itertuples()])

            counts = {}
            for t in ["categories", "locations", "providers", "services", "service_requests"]:
                cur.execute(f"SELECT count(*) FROM {t}")
                counts[t] = cur.fetchone()[0]
        return counts
    finally:
        conn.close()


if __name__ == "__main__":
    for table, n in load().items():
        print(f"{table}: {n} rows")

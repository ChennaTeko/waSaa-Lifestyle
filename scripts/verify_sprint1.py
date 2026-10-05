"""End-to-end Sprint 1 demo check. Run: python -m scripts.verify_sprint1
Prints PASS/FAIL for each stage of RAW -> CLEANED -> VALIDATED -> POSTGRESQL -> NLP-READY -> GIT."""
import subprocess

import pandas as pd

from src.utils import config

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


raw = pd.read_csv(config.RAW_SERVICES, dtype=str, keep_default_na=False) if config.RAW_SERVICES.exists() else None
check("1. RAW data present", raw is not None and len(raw) > 0, f"({0 if raw is None else len(raw)} rows)")

for label, path in [("2. CLEANED data", config.CLEANED), ("3. VALIDATED data", config.VALIDATED)]:
    check(label, path.exists(), f"({len(pd.read_csv(path))} rows)" if path.exists() else "(run the pipeline)")

if config.VALIDATED.exists():
    v = pd.read_csv(config.VALIDATED)
    check("3b. No invalid ratings/prices in validated data",
          bool(v["rating_avg"].dropna().between(0, 5).all()
               and (v["price_min"].dropna() >= 0).all()
               and (v["price_min"].fillna(0) <= v["price_max"].fillna(1e9)).all()))
    check("3c. Every record labelled with data_origin", bool(v["data_origin"].isin(config.DATA_ORIGINS).all()))

try:
    import psycopg2
    conn = psycopg2.connect(config.database_url())
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM services")
    n_services = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM service_requests")
    n_queries = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM services s LEFT JOIN providers p USING (provider_id) WHERE p.provider_id IS NULL")
    orphans = cur.fetchone()[0]
    check("4. POSTGRESQL loaded", n_services > 0, f"({n_services} services, {n_queries} test queries)")
    check("4b. No orphan foreign keys", orphans == 0)
    cur.execute("SELECT count(*) FROM services WHERE nlp_text IS NULL OR nlp_text = ''")
    check("5. NLP-READY text in database", cur.fetchone()[0] == 0)
    conn.close()
except Exception as exc:  # noqa: BLE001
    check("4. POSTGRESQL reachable", False, f"({type(exc).__name__}: {str(exc).splitlines()[0]})")

check("5b. nlp_ready.csv exists", config.NLP_READY.exists())

try:
    log = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True, cwd=config.ROOT)
    commits = [l for l in log.stdout.splitlines() if l.strip()]
    check("6. GIT version control", len(commits) >= 1, f"({len(commits)} commits)")
except FileNotFoundError:
    check("6. GIT installed", False)

print(f"\n{sum(results)}/{len(results)} checks passed")
raise SystemExit(0 if all(results) else 1)

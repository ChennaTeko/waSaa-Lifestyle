# WaSaa: NLP-Based Lifestyle Service Discovery and Provider Matching (Prototype)

Final-year project, BSc Informatics and Computer Science, Strathmore University.
This repo holds the **Sprint 1** foundation: data preparation, database and dev environment.
The NLP matching engine (TF-IDF + cosine similarity) is Sprint 2.

> **Data honesty:** all providers and services in `data/raw/` are FICTIONAL, prototype
> (`data_origin = 'synthetic'`) data. They are not real businesses. Every record is labelled.

## Pipeline
RAW (`data/raw`) -> CLEANED -> VALIDATED -> POSTGRESQL -> NLP-READY text -> Git

## Setup (Windows PowerShell shown; use `source venv/bin/activate` on Mac/Linux)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env        # then edit .env with your PostgreSQL password
```
Create the database once (in psql or pgAdmin): `CREATE DATABASE wasaa;`

## Run
```
python -m scripts.generate_seed_data   # writes data/raw/*.csv
python -m src.data.pipeline            # raw -> cleaned -> validated -> nlp_ready
python -m src.database.load            # loads PostgreSQL
python -m scripts.verify_sprint1       # demo checklist, all PASS expected
pytest -v                              # unit + pipeline tests
```

## Layout
- `data/` raw and processed data (see `data/README.md`)
- `database/schema.sql` PostgreSQL schema (7 tables)
- `src/data` cleaning, validation, pipeline; `src/nlp` text preparation; `src/database` loader; `src/utils` config
- `tests/` pytest suite; `scripts/` runnable helpers; `docs/` specification, decisions, report
- `.github/workflows/ci.yml` runs the tests automatically on every push

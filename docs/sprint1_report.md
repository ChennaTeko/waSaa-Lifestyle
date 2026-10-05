# Sprint 1 Report: Data Preparation and Environment Setup

## Checklist
- [ ] Python virtual environment created, `pip install -r requirements.txt` works
- [ ] PostgreSQL database `wasaa` created, `.env` configured (not committed)
- [ ] Git repo initialised, pushed to GitHub, several meaningful commits
- [ ] `python -m scripts.generate_seed_data` produces raw CSVs
- [ ] `python -m src.data.pipeline` shows rejected rows > 0 and valid rows > 0
- [ ] `python -m src.database.load` loads 5 categories, 12 locations, ~36 providers, 42 services, 24 queries
- [ ] `pytest -v` all pass
- [ ] `python -m scripts.verify_sprint1` all PASS
- [ ] GitHub Actions run is green
- [ ] Decision log, data requirements spec and this report in `docs/`

## How the components support the objectives and lecturer feedback
| Component | Research gap / feedback addressed | Objective supported |
|---|---|---|
| Unified `providers`/`services`/`categories` schema across 5 categories | Platform fragmentation (Section 2.6, gap 1) | Obj. iii: centralised marketplace design |
| `nlp_text` field and cleaned descriptions | Keyword-only search misses intent | Obj. v: NLP-based recommendation |
| `service_requests` (24 typed test queries) + `relevance_labels` table | Methodology feedback: how the engine is validated and evaluated | Obj. v |
| Price fields (KES) and `rating_avg`/`review_count` | Price opacity and trust gaps | Obj. ii and iii |
| Validation rules and `rejected_rows.csv` | Data quality and reproducibility | All |
| `data_origin` on every record | Honest reporting of prototype data (Section 1.7, limitation 3) | All |
| pytest + GitHub Actions | CI practice stated in Section 3.3.5 | Methodology |

## Planned evaluation (answers methodology comment, to be built in Sprint 2)
TF-IDF has no training phase: it is fitted on the service corpus. Validation: tune preprocessing choices on half of the 24 queries. Evaluation: judge candidates per query (relevance 0/1/2), report Precision@5, Recall@5 and nDCG@5 on the held-out half, compare against a keyword-matching baseline, and optionally against Sentence-BERT.

## Known limitations
All data is synthetic; labels are by a single annotator; English only; collaborative filtering out of scope.

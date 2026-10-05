# Project Decision Log
| # | Date | Decision | Reason |
|---|------|----------|--------|
| 1 | 2026-10-05 | TF-IDF + cosine similarity is the NLP baseline | Explainable, no training data needed, laptop-friendly, evaluable with ranking metrics |
| 2 | 2026-10-05 | Sentence-BERT is an optional Sprint 2+ comparison | Keeps alignment with proposal (BERT) without risking the baseline |
| 3 | 2026-10-05 | Swahili excluded; English only | No labelled Swahili service data; timeline. Supervisor to be informed |
| 4 | 2026-10-05 | Collaborative filtering excluded from prototype | No user interaction data exists yet |
| 5 | 2026-10-05 | `data_origin` tracked per record (public/synthetic/hybrid) | Academic honesty; synthetic data is never presented as real |
| 6 | 2026-10-05 | Sprint 1 uses a hand-written synthetic seed dataset | No suitable Nairobi lifestyle-services dataset identified yet; public data can be added later as `public`/`hybrid` |
| 7 | 2026-10-05 | Minimum description length set to 10 words | Short enough for realistic listings, long enough to give TF-IDF signal (spec said 15; update spec) |

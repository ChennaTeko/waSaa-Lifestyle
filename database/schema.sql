-- WaSaa Sprint 1 schema (PostgreSQL). Safe to re-run: drops and recreates tables.
DROP TABLE IF EXISTS relevance_labels, matches, service_requests, services,
                     providers, locations, categories CASCADE;

CREATE TABLE categories (
    category_id   SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city        TEXT NOT NULL,
    area        TEXT NOT NULL,
    UNIQUE (city, area)
);

CREATE TABLE providers (
    provider_id   SERIAL PRIMARY KEY,
    provider_name TEXT NOT NULL,
    location_id   INTEGER NOT NULL REFERENCES locations(location_id),
    rating_avg    NUMERIC(2,1) CHECK (rating_avg BETWEEN 0 AND 5),
    review_count  INTEGER CHECK (review_count >= 0),
    data_origin   TEXT NOT NULL CHECK (data_origin IN ('public','synthetic','hybrid')),
    UNIQUE (provider_name, location_id)
);

CREATE TABLE services (
    service_id        INTEGER PRIMARY KEY,
    provider_id       INTEGER NOT NULL REFERENCES providers(provider_id),
    category_id       INTEGER NOT NULL REFERENCES categories(category_id),
    service_name      TEXT NOT NULL,
    description       TEXT NOT NULL,
    keywords          TEXT,
    price_min         NUMERIC(10,2) CHECK (price_min >= 0),
    price_max         NUMERIC(10,2),
    price_currency    CHAR(3) NOT NULL DEFAULT 'KES',
    availability_days TEXT,
    nlp_text          TEXT NOT NULL,
    data_origin       TEXT NOT NULL CHECK (data_origin IN ('public','synthetic','hybrid')),
    CHECK (price_max IS NULL OR price_min IS NULL OR price_min <= price_max),
    UNIQUE (provider_id, service_name)
);

-- Test queries (manually written). Used for evaluation in Sprint 2.
CREATE TABLE service_requests (
    request_id          SERIAL PRIMARY KEY,
    query_text          TEXT NOT NULL,
    query_type          TEXT NOT NULL CHECK (query_type IN
                        ('clear','vague','synonym','multi-intent','typo','price-aware')),
    target_category     TEXT,
    location_constraint TEXT,
    budget_max          NUMERIC(10,2),
    language            CHAR(2) NOT NULL DEFAULT 'en',
    created_by          TEXT NOT NULL DEFAULT 'manual',
    created_at          TIMESTAMP NOT NULL DEFAULT now()
);

-- Ground-truth judgements (filled in Sprint 2).
CREATE TABLE relevance_labels (
    request_id INTEGER NOT NULL REFERENCES service_requests(request_id),
    service_id INTEGER NOT NULL REFERENCES services(service_id),
    relevance  SMALLINT NOT NULL CHECK (relevance IN (0,1,2)),
    labelled_by TEXT NOT NULL,
    notes      TEXT,
    PRIMARY KEY (request_id, service_id)
);

-- Model output (filled in Sprint 2).
CREATE TABLE matches (
    match_id   SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES service_requests(request_id),
    service_id INTEGER NOT NULL REFERENCES services(service_id),
    score      NUMERIC(6,5) NOT NULL,
    rank       INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_services_category ON services(category_id);
CREATE INDEX idx_services_provider ON services(provider_id);

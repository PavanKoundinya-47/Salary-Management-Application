# Architecture and design trade-offs

## Shape

```text
React + TypeScript (Vite)
       | HTTP / JSON
       v
FastAPI application  ---- OpenAPI docs
       | SQLAlchemy
       v
PostgreSQL 16 (Docker Compose)
       ^
 deterministic 10,000-row seed script
```

## Decisions

- **Relational database:** employee identity and salary fields have clear constraints and relationships; SQL is a natural fit. PostgreSQL is the local target, with SQLite as a convenient development/test option.
- **FastAPI + Pydantic:** typed request/response validation, clear endpoint contracts, and generated API docs reduce integration ambiguity.
- **Server-side pagination/filtering:** the full 10,000-person directory is not downloaded to the browser. `page_size` is bounded at 100, and search/filtering happens in SQL.
- **Indexes:** unique/indexed employee code and email plus indexes for name and common department/country/status filters support lookup patterns. Search over multiple columns with `ILIKE` is appropriate at this assessment scale; a larger deployment might use trigram indexes or dedicated search.
- **Currency-aware analytics:** average/min/max are grouped by currency and country. No cross-currency total is shown because the app has no FX-rate provider, rate timestamp, or policy for conversion.
- **Deterministic seed:** a fixed random seed and generated employee codes make demos and test reproduction predictable. Existing employee codes are skipped so rerunning the script doesn't create duplicates.
- **Thin frontend:** React state + fetch keeps the assessment easy to run and review. A query-cache library and design-system package could be justified for a larger product but add little value here.
- **No AI for the first release:** the assessment evaluates product judgment, not an AI requirement. Transparent database aggregates answer common pay-distribution questions reliably and are easier to test than LLM-generated salary analysis.

## Data integrity and risks

- Database uniqueness is the final authority for employee code/email collisions; the API maps conflicts to HTTP 409.
- Salary must be positive and is stored as a fixed-point numeric value rather than binary floating point in the database.
- Pydantic validates statuses and currency code length; production should add a canonical ISO currency allowlist, country/currency policy, and stronger normalization.
- A salary change currently updates the row in place. Production salary management should preserve effective-dated compensation history, who changed it, why, and approvals.
- CORS is configured for the local UI origin. Production must use explicit deployment origins, TLS, authentication, authorization, rate limiting, secrets management, backups, and monitoring.

## Scaling to 10,000 employees

10,000 rows is modest for PostgreSQL. The application applies pagination in SQL, uses indexes for frequent predicates, and computes aggregate queries in the database. Before much larger workloads, inspect query plans, add `pg_trgm` indexes if substring search becomes slow, cache expensive analytics where freshness permits, and use migrations (e.g. Alembic) rather than `create_all`.

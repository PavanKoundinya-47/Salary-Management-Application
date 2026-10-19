# Incubyte Salary Management Assessment

A full-stack salary-management dashboard for an HR manager overseeing a global workforce. Built to the uploaded **Salary Management Assessment — Candidates** brief: React UI, relational database, 10,000-person seed script, meaningful tests, and implementation artifacts. “People Ledger” is the demo workspace name, not a claim about an official Incubyte product.

## Features

- Search employee names, email, role, and employee ID; filter by country, department, and status.
- Paginated employee directory with compensation and status.
- Update annual salary and immediately refresh aggregate analytics.
- Global workforce KPIs and breakdowns by department, country, and currency.
- CSV export for the currently visible page.
- Deterministic seed script that creates 10,000 employees and can be rerun without duplicating employee codes.
- FastAPI OpenAPI docs, PostgreSQL persistence, health endpoint, and API tests.

## Run locally with Docker

Prerequisites: Docker Desktop / Docker Engine and Compose plugin.

```bash
cp .env.example .env                 # optional: change local development password
# Start database + API
docker compose up --build -d db api
# Seed the 10,000 demo employees
docker compose --profile seed run --rm seed
# Start the UI (in a second terminal)
cd frontend
npm install
npm run dev
```

Open the dashboard at <http://localhost:5174>. API docs: <http://localhost:8001/docs>. Health: <http://localhost:8001/health>.

To stop services: `docker compose down`. To remove the local database volume too: `docker compose down -v` (destructive).

## Run backend without Docker (SQLite development mode)

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The default local database is `backend/salary_management.db` when launched from `backend/`. In another terminal seed it with `cd backend && python seed.py`. For PostgreSQL, set `DATABASE_URL` to a SQLAlchemy URL such as `postgresql+psycopg://salary_app:password@localhost:5432/salary_management`.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

Tests cover health, search/listing, salary update, and the currency-aware analytics contract. The API test uses a local SQLite database and doesn't require a running PostgreSQL server. For repeatable isolated runs, delete `backend/test_salary_management.db` before running tests. The app uses a relational schema with indexed fields and server-side pagination.

## API overview

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/api/employees` | Search, filter, and paginate employees (`q`, `country`, `department`, `status`, `page`, `page_size`) |
| POST | `/api/employees` | Create employee (employee code and email must be unique) |
| PATCH | `/api/employees/{id}` | Update salary, department, job title, or status |
| GET | `/api/analytics` | Headcount and salary aggregates by currency/country/department |
| GET | `/api/filters` | Distinct filter options |

Example salary update:

```bash
curl -X PATCH http://localhost:8001/api/employees/1 \
  -H 'Content-Type: application/json' \
  -d '{"annual_salary": 1450000.00}'
```

## Requirements and scope

See [`docs/requirements.md`](docs/requirements.md) for the one-page pre-build requirements document. Architecture and product decisions are in [`docs/design-decisions.md`](docs/design-decisions.md), the demo walkthrough is in [`docs/demo-script.md`](docs/demo-script.md), and [`docs/ai-usage.md`](docs/ai-usage.md) records the AI-assisted workflow and verification checklist.

## Known limitations / production hardening

- Authentication, role-based access, approval workflow, audit log, and encryption/key management are intentionally not implemented in this assessment demo. Salary data is sensitive; do not expose this demo to public traffic or real employee data.
- Salary comparisons are grouped by currency. The system deliberately does not add INR to USD or imply a conversion without an exchange-rate source and effective date.
- CSV export exports the current visible page, not all filtered records; a production version should provide a server-side export endpoint with authorization and audit logging.
- Demo seed data is synthetic. Country assignment and salaries are plausible fixtures, not compensation policy or market benchmarks.
- No deployment or demo video is claimed by this repository artifact. Deploy it to a host of your choice and record the walkthrough before submission.

## Git history requirement

The assessment explicitly asks for incremental commits. This generated directory is not a pre-authored commit history. Create a repository and commit the work in reviewable stages rather than manufacturing past timestamps:

```bash
git init
git add docs/requirements.md && git commit -m "docs: define salary management scope"
git add backend && git commit -m "feat: implement employee API and seed data"
git add frontend && git commit -m "feat: build HR salary dashboard"
git add docs README.md docker-compose.yml .env.example .gitignore && git commit -m "test: document tradeoffs and local run workflow"
```

Use meaningful real commits as you iterate; do not present these suggested commits as history that already exists.

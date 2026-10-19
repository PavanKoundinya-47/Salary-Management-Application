# Incubyte Salary Management Assessment

A full-stack salary-management dashboard for an HR manager overseeing a global workforce. Built to the uploaded **Salary Management Assessment — Candidates** brief: React UI, relational database, 10,000-person seed script, meaningful tests, and implementation artifacts. “People Ledger” is the demo workspace name, not a claim about an official Incubyte product.

## Live Application & Demo Videos

- **Live Application:** [Open Salary Management Dashboard](https://salary-management-application.vercel.app/)
- **Source Code:** [GitHub Repository](https://github.com/PavanKoundinya-47/Salary-Management-Application)

### Video Walkthroughs

- **Demo & Deployment Walkthrough:** [Watch Deployment Video](<https://drive.google.com/file/d/12IYbRZArgUkpBwwRXJsVTDeVWXul2eDz/view?usp=sharing>)

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

## Requirements and Design Documentation

The repository includes the following implementation artifacts:

- [Requirements document](docs/requirements.md) — pre-build requirements and scope.
- [Design decisions](docs/design-decisions.md) — architecture, trade-offs, and product decisions.
- [Demo script](docs/demo-script.md) — application walkthrough.
- [AI usage documentation](docs/ai-usage.md) — AI-assisted workflow and verification checklist.

## Deployment

The application is deployed using:

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** PostgreSQL on Render

Production URLs:

- Frontend: [Salary Management Dashboard](https://salary-management-application.vercel.app/)
- Backend health: [Health Check](https://salary-management-application.onrender.com/health)
- Analytics API: [Analytics Endpoint](https://salary-management-application.onrender.com/api/analytics)

## Known Limitations and Production Hardening

- Authentication, role-based access control, approval workflows, audit logs, and encryption/key management are not implemented in this assessment demo.
- Salary data is sensitive. Use synthetic data only and do not expose real employee information through this public demo.
- Salary comparisons are grouped by currency. The application does not add INR to USD or imply currency conversion without an exchange-rate source and effective date.
- CSV export covers the current visible page rather than all filtered records. A production version should provide a server-side export endpoint with authorization and audit logging.
- Seed data is synthetic. Country assignments and salaries are plausible fixtures, not compensation policy or market benchmarks.
- Deployment and demo walkthroughs are available in the **Live Application & Demo Videos** section above.

## License

No license has been specified for this project. All rights remain with the repository owner unless a license is added.
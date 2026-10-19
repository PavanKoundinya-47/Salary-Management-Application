# Salary Management — Requirements (v1)

## Goal
Replace spreadsheet-based salary tracking with a web workspace that lets an HR manager manage employee compensation and answer basic workforce-pay questions across a 10,000-person, multi-country organization.

## Primary user
HR Manager / HR Administrator responsible for finding employee records, maintaining salary data, and understanding how compensation is distributed.

## In scope
- Store employee identity, employee code, department, job title, country, currency, annual salary, and employment status in a relational database.
- Seed 10,000 synthetic employee records with a deterministic, repeatable script.
- Search by employee name, email, role, or employee code; filter by country, department, and status; paginate results server-side.
- Update annual salary and a small set of employee attributes with input validation and clear feedback.
- Provide a dashboard with total/active headcount, countries, departments, salary ranges/averages by currency, country-level salary aggregates, and department headcount.
- Expose documented HTTP APIs, health check, deterministic automated tests, and local Docker setup.
- Include architecture/trade-off notes and a demo walkthrough.

## Deliberately out of scope (and why)
- Payroll execution, payslips, tax calculations, benefits, bonuses, deductions, and statutory compliance: these require jurisdiction-specific rules and integrations beyond a focused assessment.
- Authentication, fine-grained authorization, approval workflows, and audit trails: essential before real use, but would distract from demonstrating the core data-management workflow. This demo must not be exposed publicly with real data.
- FX conversion and a single global salary total: combining currencies without dated exchange rates is misleading. Analytics are explicitly grouped by currency.
- Bulk imports from legacy spreadsheets, file attachments, notifications, and HRIS integrations: useful follow-up work, not required to validate the core workflow.
- AI/natural-language salary querying: the brief asks the HR manager to answer questions about pay, but does not require an AI integration. Structured filters and transparent grouped analytics are more deterministic for this first version.

## Success criteria
1. A clean local setup starts the database and API; the UI connects and displays seeded data.
2. The seed script yields 10,000 unique employee codes and emails and is safe to rerun.
3. HR can search/filter/page employee records and update a salary.
4. Dashboard metrics derive from database queries and salary aggregations never mix currencies.
5. Tests are fast, understandable, and cover core API behavior.
6. The repository contains requirements, design tradeoffs, AI-use notes, and a demo script; deployment and a recorded demo are completed before submission.

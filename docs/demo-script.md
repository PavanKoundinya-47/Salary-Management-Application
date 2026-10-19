# Interview demo walkthrough (3–5 minutes)

1. **Frame the problem (20s):** HR is moving a 10,000-person multi-country salary spreadsheet into a searchable workspace.
2. **Show the overview (40s):** explain headcount, active employees, country/department counts, and currency-specific salary bands. Explicitly point out that different currencies are not added together.
3. **Find a person (45s):** search an employee code or name, then filter by department and country. Explain server-side pagination.
4. **Update compensation (45s):** click Edit, change annual salary, save, and show the refreshed salary row and analytics.
5. **Show the API (30s):** open `/docs`, demonstrate `GET /api/employees`, `PATCH /api/employees/{id}`, and `/api/analytics`.
6. **Show engineering quality (45s):** explain the deterministic seed, run `pytest -q`, and show requirements/design tradeoffs.
7. **Close with deliberate exclusions (30s):** mention auth/authorization, audit history, approval workflow, payroll/tax, and deployment as explicit production follow-ups—not silently ignored needs.

Record the actual working software, not a mockup. Verify API and UI are running before recording.

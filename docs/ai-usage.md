# AI-assisted development notes

This project was drafted with an AI coding assistant and should be treated as a code-reviewable starting point, not as proof that generated code is correct.

## Intent
- Convert the assessment brief into a small, explicit requirements document before implementation.
- Generate a thin full-stack slice: relational schema, API contracts, deterministic seed, dashboard, tests, and run instructions.
- Prefer transparent SQL analytics over adding an unnecessary LLM layer.

## Human verification checklist before submission
- [ ] Run `docker compose up --build -d db api` and confirm `/health`.
- [ ] Run the seed profile and verify exactly 10,000 employee rows on a fresh database.
- [ ] Run backend tests from a clean checkout.
- [ ] Run `npm install && npm run build` and manually verify the dashboard, search, filters, pagination, salary edit, and CSV export.
- [ ] Review validation, SQL errors, accessibility, responsive behavior, and browser console.
- [ ] Add authentication, authorization, audit history, and secret management if the app will handle anything other than synthetic data.
- [ ] Create genuine incremental Git commits, deploy the app, record a demo, and share repository/deployment links.

## Prompting principles
- Use the assessment's exact user/problem statement as the source of truth.
- Ask for a plan and explicit exclusions before asking for implementation.
- Ask the assistant to explain currency handling, validation, query performance, and test strategy.
- Verify generated artifacts with tests and manual review; do not claim deployment, test success, or commit history without evidence.

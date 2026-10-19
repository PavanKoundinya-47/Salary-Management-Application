.PHONY: up seed down test frontend-build
up:
	docker compose up --build -d db api
seed:
	docker compose --profile seed run --rm seed
down:
	docker compose down
test:
	cd backend && pytest -q
frontend-build:
	cd frontend && npm install && npm run build

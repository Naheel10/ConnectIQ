dev:
	docker compose up --build

backend-test:
	docker compose run --rm backend pytest -q

migrate:
	docker compose run --rm backend alembic upgrade head

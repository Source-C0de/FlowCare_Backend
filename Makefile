.PHONY: install dev lint format type test up down

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

format:
	ruff format .

lint:
	ruff check .

type:
	mypy .

test:
	pytest -q

up:
	docker compose up --build

down:
	docker compose down -v

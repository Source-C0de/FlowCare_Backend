.PHONY: install dev lint format type test up down

install:
	./venv/bin/pip install -r requirements.txt

dev:
	./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

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


# Database migration (always use project venv)
migration:
	./venv/bin/alembic revision --autogenerate -m "$(msg)"

upgrade:
	./venv/bin/alembic upgrade head

downgrade:
	./venv/bin/alembic downgrade -1

history:
	./venv/bin/alembic history

current:
	./venv/bin/alembic current



# Git
add:
	git add .

pull:
	git pull origin master

push:
	git push origin master
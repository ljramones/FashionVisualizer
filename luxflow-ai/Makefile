.PHONY: backend frontend test lint seed tree

backend:
	uvicorn backend.app.main:app --reload

frontend:
	npm --prefix frontend run dev

test:
	python -m pytest backend/tests

lint:
	ruff check backend scripts
	npm --prefix frontend run lint

seed:
	python scripts/seed_sample_catalog.py

tree:
	find . -maxdepth 4 -type f | sort

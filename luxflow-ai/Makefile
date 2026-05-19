.PHONY: backend frontend test lint seed tree

PYTHON ?= .venv/bin/python
UVICORN ?= .venv/bin/uvicorn
RUFF ?= .venv/bin/ruff
NPM ?= npm

backend:
	$(UVICORN) backend.app.main:app --reload

frontend:
	$(NPM) --prefix frontend run dev

test:
	$(PYTHON) -m pytest backend/tests

lint:
	$(RUFF) check backend scripts
	$(NPM) --prefix frontend run lint

seed:
	$(PYTHON) scripts/seed_sample_catalog.py

tree:
	find . -maxdepth 4 -type f | sort

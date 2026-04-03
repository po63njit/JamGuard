.PHONY: install test lint typecheck format

install:
	python -m pip install -e .[dev]

test:
	pytest -q

lint:
	ruff check src tests scripts

typecheck:
	mypy src

format:
	ruff format src tests scripts

CONFIG ?= config.json

install:
	uv sync

run:
	uv run pac-man.py $(CONFIG)

debug:
	uv run python3 -m pdb pac-man.py $(CONFIG)

clean:
	uv clean
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 --exclude .venv,.mypy_cache && mypy . --exclude .venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 --exclude .venv,.mypy_cache && mypy . --exclude .venv --strict

.PHONY: install run debug clean lint lint-strict
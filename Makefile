all: deps lint format test

deps:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

format: deps
	ruff format .

lint: deps
	ruff check --fix --output-format full .

test: deps
	AUTOKITTEH_UNIT_TEST=1 pytest -v .

.PHONY: all deps format lint test

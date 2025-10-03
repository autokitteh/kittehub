# The Makefile is for local development only.

.PHONY: all
all: lint typecheck test format

.PHONY: lint
lint:
	uvx ruff check

.PHONY: format
format:
	uvx ruff format --check

.PHONY: typecheck
typecheck:
	uvx --with autokitteh --with gspread --with google-api-python-client --with twilio --with pytest --with slack-sdk mypy --follow-untyped-imports .

.PHONY: test
test:
	uvx pytest

.PHONY: deploy
deploy:
	akl deploy --manifest autokitteh.yaml

# All of these packages are builtin into autokitteh SDK.
UVX=uvx --with autokitteh \
		--with gspread \
		--with google-api-python-client \
		--with google-generativeai \
		--with twilio \
		--with pytest \
		--with slack-sdk
		

.PHONY: all
all: lint typecheck test format

.PHONY: lint
lint:
	$(UVX) ruff check --config ../pyproject.toml

.PHONY: format
format:
	$(UVX) ruff format --check --config ../pyproject.toml

.PHONY: typecheck
typecheck:
	$(UVX) mypy --follow-untyped-imports  .

.PHONY: test
test:
	$(UVX) pytest

.PHONY: deploy
deploy:
	ak deploy --manifest autokitteh.yaml

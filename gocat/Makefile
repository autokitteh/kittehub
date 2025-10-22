UVX=uvx --with autokitteh --with gspread

.PHONY: all
all: lint typecheck format

.PHONY: lint
lint:
	$(UVX) ruff check --config ../pyproject.toml --ignore I001

.PHONY: format
format:
	$(UVX) ruff format --check --config ../pyproject.toml

.PHONY: typecheck
typecheck:
	$(UVX) mypy --follow-untyped-imports  .


.PHONY: deploy
deploy:
	ak deploy --manifest autokitteh.yaml

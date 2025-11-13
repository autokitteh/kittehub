UVX=uvx --with autokitteh --with pytest --with anthropic==0.71.0 --with rapidfuzz

.PHONY: all
all: lint typecheck test format

.PHONY: lint
lint:
	$(UVX) ruff check --config ../pyproject.toml --ignore I001

.PHONY: format
format:
	$(UVX) ruff format --check --config ../pyproject.toml

.PHONY: typecheck
typecheck:
	$(UVX) mypy --follow-untyped-imports  .

.PHONY: test
test:
	$(UVX) pytest -s

.PHONY: data
data:
	./_gendata.sh

.PHONY: deploy
deploy:
	ak deploy --manifest autokitteh.yaml

format:
	uv run ruff format

lint:
	uv run ruff check --fix
	uv run mypy --ignore-missing-imports --install-types --non-interactive --package stcaf

test:
	uv run pytest --verbose --color=yes tests

validate: format lint test

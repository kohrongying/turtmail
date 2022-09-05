
.PHONY: lint
lint:
	ruff src/**/*.py tests/**/*.py

.PHONY: fmt
fmt:
	black src tests

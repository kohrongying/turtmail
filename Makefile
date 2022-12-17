
.PHONY: lint
lint:
	ruff payslip_mailer/**/*.py

.PHONY: lint-fix
lint-fix:
	ruff payslip_mailer/**/*.py --fix

.PHONY: fmt
fmt:
	black payslip_mailer

.PHONY: test
test:
	python -m pytest .

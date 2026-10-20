.DEFAULT_GOAL := all
DESIGN_SYSTEM_VERSION="73.12.0"
BUILD_TIME=$(shell date +%s)
GIT_COMMIT=$(shell git rev-parse HEAD)
VERSION ?= $(shell git tag --points-at HEAD | grep ^v | head -n 1)

.PHONY: all
all: ## Show the available make targets.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: clean
clean: ## Clean the temporary files.
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf megalinter-reports

.PHONY: format
format:  ## Format the code.
	poetry run ruff check . --fix
	poetry run ruff format .

.PHONY: lint
lint:  ## Run all linters (ruff/pylint/mypy).
	poetry run ruff check .
	poetry run ruff format --check .
	make mypy

.PHONY: pre-commit
pre-commit:  ## Run all pre-commit hooks across the repository.
	poetry run pre-commit run --all-files

.PHONY: install-pre-commit
install-pre-commit:  ## Install the local git pre-commit hooks.
	poetry run pre-commit install

.PHONY: test
test:  ## Run the tests and check coverage.
	poetry run pytest -n auto --cov=dis_frontend_dataset_controller --cov-report term-missing --cov-fail-under=80

.PHONY: mypy
mypy:  ## Run mypy.
	poetry run mypy dis_frontend_dataset_controller

.PHONY: run
run:  ## Run the python script
	poetry run python -m dis_frontend_dataset_controller

.PHONY: install
install:  ## Install the dependencies excluding dev.
	poetry install --only main

.PHONY: install-dev
install-dev:  ## Install the dependencies including dev.
	poetry install

.PHONY: megalint
megalint:  ## Run the mega-linter. Use LINTER=NAME to run only one.
	docker run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		$(if $(LINTER),-e ENABLE_LINTERS=$(LINTER),) \
		ghcr.io/oxsecurity/megalinter:v9

.PHONY: debug
debug:
	./scripts/load-design-system-templates.sh $(DESIGN_SYSTEM_VERSION)
	BUILD_TIME=$(BUILD_TIME) VERSION=$(VERSION) GIT_COMMIT=$(GIT_COMMIT) flask --app dis_frontend_dataset_controller/app run

## Include project environment variables if necessary
# include .env

SHELL = /bin/bash


PYTHON_VERSION = 3.10
PYTHON = python${PYTHON_VERSION}


.DEFAULT_GOAL := help

.PHONY: check-system
check-system: ## Check system for necessary tools
	@echo ">>> Checking python..."
	@${PYTHON} --version || { echo ">>> $(PYTHON) must be installed !"; exit 1; }
	@echo ">>> OK."
	@echo ""

.PHONY: venv
venv: check-system ## Create virtual environment with venv
	@echo ">>> Creating virtual environment : '$(PWD)/env' ..."
	${PYTHON} -m venv env
	@echo ">>> OK."
	@echo ""

	@echo "!!! Activate with : 'source env/bin/activate' !!!"
	@echo ""

.PHONY: clean-venv
clean-venv: ## Remove virtual environment
	@echo ">>> Removing virtual environment : '$(PWD)/env' ..."
	rm -rf env
	@echo ">>> OK."
	@echo ""

.PHONY: check-venv
check-venv: ## Check that virtual environment is active
	@echo ">>> Checking that this project's virtual environment is active : '$(PWD)/env' ..."
	@${PYTHON} -c "import sys; sys.exit(0) if (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)) else sys.exit(1)" || { \
		echo ">>> ERROR : Virtual environment must be active !"; \
		echo ">>> Activate with : 'source env/bin/activate' ."; \
		echo ""; \
		exit 1; \
	}
	@test "$(VIRTUAL_ENV)" = "$(PWD)/env" || { \
		echo ">>> ERROR : Virtual environment must be '$(PWD)/env' !"; \
		echo ">>> Deactivate active venv ('$(VIRTUAL_ENV)') with : 'deactivate' ."; \
		echo ">>> Activate this project's venv with : 'source env/bin/activate' ."; \
		echo ""; \
		exit 1; \
	}
	@echo ">>> OK."
	@echo ""

requirements-dev.txt: check-system check-venv ## Create requirements-dev.txt file
	@echo ">>> Creating 'requirements-dev.txt' file..."
	pip install --upgrade pip
	pip install --upgrade isort black black flake8 bandit mypy \
		pytest pytest-cov
	pip freeze | grep -v "pkg_resources" > requirements-dev.txt
	@echo ">>> OK."
	@echo ""

requirements.txt: check-system check-venv ## Create requirements.txt file
	@echo ">>> Creating 'requirements.txt' file..."
	pip install --upgrade requests fastapi uvicorn pydantic[dotenv] sqlalchemy
	pip freeze | grep -v "pkg_resources" > requirements.txt
	@echo ">>> OK."
	@echo ""

.PHONY: deps-dev
deps-dev: check-system check-venv requirements-dev.txt ## Install dependencies with pip
	@echo ">>> Installing dev dependancies from 'requirements-dev.txt' file..."
	pip install -r requirements-dev.txt
	@echo ">>> OK."
	@echo ""

.PHONY: deps
deps: check-system check-venv requirements.txt ## Install dependencies with pip
	@echo ">>> Installing dependancies from 'requirements.txt' file..."
	pip install -r requirements.txt
	@echo ">>> OK."
	@echo ""

.PHONY: install
install: check-system check-venv deps-dev deps ## Check system and venv, and install dependencies

.PHONY: start
start: ## Serve app with uvicorn
	@echo ">>> Starting uvicorn server..."
	uvicorn src.main:app --reload
	@echo ">>> OK."
	@echo ""

.PHONY: isort
isort: ## Sort imports with Isort
	@echo ">>> Sorting imports..."
	isort src/ tests/
	@echo ">>> OK."
	@echo ""

.PHONY: format
format: ## Format with Black
	@echo ">>> Formatting code..."
	black src/ tests/
	@echo ">>> OK."
	@echo ""

.PHONY: lint
lint: ## Lint with Flake8
	@echo ">>> Linting code..."
	flake8 --count --show-source --statistics src/ tests/
	@echo ">>> OK."
	@echo ""

.PHONY: bandit
bandit: ## Check security Bandit
	@echo ">>> Checking security ..."
	bandit --recursive src/
	@echo ">>> OK."
	@echo ""

.PHONY: mypy
mypy: ## Type check with Mypy
	@echo ">>> Checking types ..."
	mypy --install-types --non-interactive src/ tests/
	@echo ">>> OK."
	@echo ""

.PHONY: clean-mypy
clean-mypy: ## Remove Mypy cache files
	@echo ">>> Removing mypy artifacts..."
	rm -rf .mypy_cache
	@echo ">>> OK."
	@echo ""

.PHONY: test
test: ## Test and produce coverage report using pytest
	@echo ">>> Running tests and processing coverage..."
	pytest --cov-report=xml:coverage.xml --cov=src tests/
	@echo ">>> OK."
	@echo ""

.PHONY: clean-test
clean-test: ## Remove test cache and coverage files
	@echo ">>> Removing test and coverage artifacts..."
	rm -rf .coverage coverage.xml .pytest_cache
	@echo ">>> OK."
	@echo ""

.PHONY: qa
qa: isort format lint bandit mypy test ## Run the full QA process

.PHONY: clean-pycache
clean-pycache: ## Remove python cache files
	@echo ">>> Removing python artifacts..."
	find . -name __pycache__ -type d -exec rm -rf {} \;
	find . -name *.pyc -type f -exec rm -f {} \;
	@echo ">>> OK."
	@echo ""

.PHONY: clean
clean: clean-venv clean-mypy clean-test clean-pycache clean-install  ## Remove all file artifacts

.PHONY: help
help:  ## Print help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e 's/Makefile://' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

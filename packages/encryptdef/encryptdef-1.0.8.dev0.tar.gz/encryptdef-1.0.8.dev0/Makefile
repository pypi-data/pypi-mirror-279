.PHONY: install virtualenv lint fmt test clean build publish-test publish

# Detectar o sistema operacional
OS := $(shell uname)

# Variáveis para simplificar os comandos
VENV_DIR=.venv
VENV_BIN=$(VENV_DIR)/bin
PYTHON=$(VENV_BIN)/python
PIP=$(VENV_BIN)/pip

# Comando para ativar o ambiente virtual
ifeq ($(OS), Linux)
    ACTIVATE_VENV=. $(VENV_BIN)/activate
endif
ifeq ($(OS), Darwin) # macOS
    ACTIVATE_VENV=. $(VENV_BIN)/activate
endif
ifeq ($(OS), Windows_NT)
    ACTIVATE_VENV=$(VENV_DIR)\Scripts\activate
    VENV_BIN=$(VENV_DIR)\Scripts
endif

install: ## Instalar dependências para o ambiente de desenvolvimento
	@echo "Instalando dependências para o ambiente de desenvolvimento..."
	@$(PIP) install -e '.[test,dev]'

virtualenv: ## Criar ambiente virtual e instalar dependências
	@echo "Criando ambiente virtual..."
	@python -m venv $(VENV_DIR)
	@echo "Instalando dependências no ambiente virtual..."
	@$(PIP) install -e '.[test,dev]'

lint: ## Executar linters
	@echo "Executando linters..."
	@$(VENV_BIN)/mypy --ignore-missing-imports encryptdef
	@$(VENV_BIN)/pflake8

fmt: ## Formatar código
	@echo "Formatando código..."
	@$(VENV_BIN)/isort encryptdef tests
	@$(VENV_BIN)/black encryptdef tests

test: ## Rodando os Testes
	@echo "Rodando os Testes..."
	@$(VENV_BIN)/pytest --cov=encryptdef
	@$(VENV_BIN)/coverage xml
	@$(VENV_BIN)/coverage html


clean: ## Limpar arquivos desnecessários
	@echo "Limpando arquivos desnecessários..."
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

build: clean ## Construir pacotes
	@echo "Construindo pacotes..."
	@$(PYTHON) -m build 

publish-test: build ## Publicar no TestPyPI
	@echo "Publicando no TestPyPI..."
	@$(VENV_BIN)/twine upload --repository testpypi dist/*

publish: build ## Publicar no PyPI
	@echo "Publicando no PyPI..."
	@$(VENV_BIN)/twine upload dist/*

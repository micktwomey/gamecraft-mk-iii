PIP=$(VENV)/bin/pip
PIP_COMPILE=$(VENV)/bin/pip-compile
PIP_SYNC=$(VENV)/bin/pip-sync
PYTHON=$(VENV)/bin/python
SOURCE=$(shell find gamecraft -type f)
VENV=$(CURDIR)/venv

.PHONY: all
all: test

requirements.txt: requirements.in
	$(PIP_COMPILE) requirements.in

$(PYTHON):
	virtualenv -p python3.4 $(VENV)

$(PIP_SYNC): $(PIP)
	$(PIP) install -U pip-tools

$(PIP): $(PYTHON)
	$(PIP) install -U pip setuptools wheel

.PHONY: build
build: build/build.txt

build/build.txt:
	mkdir -p build
	touch build/build.txt

build/pip-installed.txt: requirements.txt build/build.txt $(PIP_SYNC) $(PIP)
	$(PIP_SYNC) requirements.txt
	$(PIP) freeze > build/pip-installed.txt

build/test.txt: build/pip-installed.txt $(SOURCE)
	$(PYTHON) manage_development.py test --settings=gamecraft.settings
	touch build/test.txt

.PHONY: test
test: build/test.txt


.PHONY: clean
clean:
	rm -rf build
	rm -rf venv
	rm -rf dist

.PHONY: sync-master-db-to-staging
sync-master-db-to-staging:
	heroku pg:copy --app gamecraft-it-staging gamecraft-it-eu::PURPLE HEROKU_POSTGRESQL_RED

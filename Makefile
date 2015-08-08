VENV=$(CURDIR)/venv
PIP_SYNC=$(VENV)/bin/pip-sync
PIP=$(VENV)/bin/pip
PYTHON=$(VENV)/bin/python
PIP_COMPILE=$(VENV)/bin/pip-compile
SOURCE=$(shell find gamecraft -type f)

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

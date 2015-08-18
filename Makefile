PIP=$(VENV)/bin/pip
PIP_COMPILE=$(VENV)/bin/pip-compile
PIP_SYNC=$(VENV)/bin/pip-sync
PYTHON=$(VENV)/bin/python
SOURCE=$(shell find gamecraft -type f)
VENV=$(CURDIR)/venv

#
# Do some jiggery pokery to set some variables from heroku
#
MAKE_SETTINGS_FILES=$(wildcard *.settings.make)
MAKE_SETTINGS_FILE=.settings.make

ifndef $(MAKE_SETTINGS_FILES)
	IGNORE:=$(shell heroku config -a gamecraft-it-staging --shell | sed -E 's/^(.*)/export \1/g' > $(MAKE_SETTINGS_FILE))
		# '
endif

include $(MAKE_SETTINGS_FILE)


.PHONY: all
all: test

requirements.txt: requirements.in
	$(PIP_COMPILE) requirements.in

.PHONY: requirements
requirements: requirements.txt

$(PYTHON):
	virtualenv -p python3.4 $(VENV)

$(PIP_SYNC): $(PIP)
	$(PIP) install -U pip-tools

$(PIP): $(PYTHON)
	$(PIP) install -U pip setuptools wheel

.PHONY: build
build: build/build.txt

.PHONY: pip-sync
pip-sync: requirements.txt $(PIP_SYNC)
	$(PIP_SYNC) requirements.txt

.PHONY: test
test: pip-sync $(SOURCE)
	$(PYTHON) manage_development.py test --settings=gamecraft.settings

.PHONY: clean
clean:
	rm -rf build
	rm -rf venv
	rm -rf dist
	rm -f $(MAKE_SETTINGS_FILE)

.PHONY: sync-master-db-to-staging
sync-master-db-to-staging:
	heroku pg:copy --app gamecraft-it-staging gamecraft-it-eu::PURPLE HEROKU_POSTGRESQL_RED

.PHONY: runserver
runserver:
	$(PYTHON) manage_development.py runserver

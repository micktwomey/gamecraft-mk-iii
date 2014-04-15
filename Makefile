SYSTEM_PYTHON=$(shell which python3.4 || which python3)
VENV=$(CURDIR)/gamecraft-mk-iii-venv
PIP=$(VENV)/bin/pip
INSTALLED=$(VENV)/installed.txt
REQUIREMENTS=$(CURDIR)/requirements.txt


all: $(INSTALLED)

$(PIP):
	virtualenv --python=$(SYSTEM_PYTHON) $(VENV)

$(INSTALLED): $(REQUIREMENTS) $(PIP)
	$(PIP) install -r $(REQUIREMENTS)
	$(PIP) freeze -r $(REQUIREMENTS) > $(INSTALLED)

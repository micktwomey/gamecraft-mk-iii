DOCKER=$(CURDIR)/docker
REQUIREMENTS=$(DOCKER)/requirements.txt

.PHONY: \
	docker

all: build

build: $(REQUIREMENTS)
	cd $(DOCKER) && $(MAKE)

migrate:
	cd $(DOCKER) && $(MAKE) migrate

runserver: stop build migrate
	cd $(DOCKER) && $(MAKE) runserver

stop:
	cd $(DOCKER) && $(MAKE) stop
	docker ps

shell:
	cd $(DOCKER) && $(MAKE) shell

test:
	cd $(DOCKER) && $(MAKE) test

createdb:
	cd $(DOCKER) && $(MAKE) createdb

dumpdata:
	cd $(DOCKER) && $(MAKE) dumpdata
	@echo
	@echo "backups/data.yaml has the data"
	@echo

loaddata:
	@echo
	@echo "Loading data from backups/data.yaml"
	@echo
	cd $(DOCKER) && $(MAKE) loaddata

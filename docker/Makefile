TAG=micktwomey/gamecraft
MOUNTS=-v /vagrant:/gamecraft/src/development:rw \
	-v /vagrant/logs:/gamecraft/logs:rw \
	-v /vagrant/uploads:/gamecraft/uploads:rw \
	-v /vagrant/backups:/gamecraft/backups:rw \
	-v /vagrant/config:/gamecraft/config:rw

LINKS=--link postgresql:postgresql

all: build

build:
	docker build -t $(TAG) .

shell:
	docker run --rm $(MOUNTS) $(LINKS) -i -t --entrypoint=/bin/bash $(TAG) -i

migrate:
	docker run --rm $(MOUNTS) $(LINKS) -i -t $(TAG) migrate

runserver:
	docker run --rm -p 8000:8000 $(MOUNTS) $(LINKS) --name gamecraft -i -t $(TAG)

runserver-background:
	docker run --rm -p 8000:8000 $(MOUNTS) $(LINKS) -d --name gamecraft $(TAG)
	docker ps
	echo
	echo Use "docker stop gamecraft" to stop
	echo
	echo Use "docker attach gamecraft" to attach to the process
	echo

stop:
	docker stop gamecraft || true
	docker rm gamecraft || true

createdb:
	@echo
	@echo Use "docker" for the password
	@echo
	docker run --rm -i -t $(LINKS) --entrypoint=/bin/bash micktwomey/postgresql -c 'createdb -E UTF-8 -T template0 -O docker -U docker -h $$POSTGRESQL_PORT_5432_TCP_ADDR -p $$POSTGRESQL_PORT_5432_TCP_PORT gamecraft'

dropdb:
	@echo
	@echo Use "docker" for the password
	@echo
	docker run --rm -i -t $(LINKS) --entrypoint=/bin/bash micktwomey/postgresql -c 'dropdb  -U docker -h $$POSTGRESQL_PORT_5432_TCP_ADDR -p $$POSTGRESQL_PORT_5432_TCP_PORT gamecraft'

dumpdata:
	docker run --rm -i -t $(MOUNTS) $(LINKS) $(TAG) dumpdata --indent=2 --format=yaml --natural-foreign  --natural-primary auth.user sites.site socialaccount | egrep -v 'RemovedInDjango18Warning|^  class SocialAppForm) > ../backups/data.yaml

loaddata:
	docker run --rm -i -t $(MOUNTS) $(LINKS) $(TAG) loaddata /gamecraft/backups/data.yaml

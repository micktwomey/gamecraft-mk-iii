MOUNTS=-v /vagrant:/gamecraft/src/development:rw \
	-v /vagrant/logs:/gamecraft/logs:rw \
	-v /vagrant/uploads:/gamecraft/uploads:rw \
	-v /vagrant/backups:/gamecraft/backups:rw \
	-v /vagrant/config:/gamecraft/config:rw
LINKS=--link postgresql:postgresql
DOCKER_RUN=docker run --rm $(MOUNTS) $(LINKS)
DOCKER_RUN_INTERACTIVE=$(DOCKER_RUN) -i -t
DOCKER_RUN_DJANGO_ADMIN=$(DOCKER_RUN_INTERACTIVE) --entrypoint=/usr/local/bin/django-admin
DOCKER_RUN_BASH=$(DOCKER_RUN_INTERACTIVE) --entrypoint=/bin/bash
TAG=micktwomey/gamecraft

all:

build:
	docker pull $(TAG):latest

migrate:
	$(DOCKER_RUN_INTERACTIVE) $(TAG) migrate

runserver:
	$(DOCKER_RUN_DJANGO_ADMIN) --name gamecraft -p 8000:8000 $(TAG) runserver 0.0.0.0:8000

uwsgi:
	$(DOCKER_RUN_INTERACTIVE) --name gamecraft -p 8000:8000 $(TAG)

shell:
	$(DOCKER_RUN_BASH) $(TAG) -i

test:
	$(DOCKER_RUN_DJANGO_ADMIN) $(TAG) test gamecraft.gamecrafts

startdb:
	docker pull micktwomey/postgresql:latest
	docker start postgresql || docker run --name postgresql -d micktwomey/postgresql

stopdb:
	docker stop postgresql

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
	$(DOCKER_RUN_DJANGO_ADMIN) $(TAG) dumpdata --indent=2 --format=json --natural-foreign  --natural-primary auth.user sites.site socialaccount | egrep -v -e 'RemovedInDjango18Warning|^\s*class SocialAppForm.*)' > backups/site_data.json
	$(DOCKER_RUN_DJANGO_ADMIN) $(TAG) dumpdata --indent=2 --format=json --natural-foreign  --natural-primary gamecrafts | egrep -v -e 'RemovedInDjango18Warning|^\s*class SocialAppForm.*)' > backups/gamecrafts.json

loaddata:
	$(DOCKER_RUN_DJANGO_ADMIN) $(TAG) loaddata /gamecraft/backups/site_data.json
	$(DOCKER_RUN_DJANGO_ADMIN) $(TAG) loaddata /gamecraft/backups/gamecrafts.json

update_fixtures: dumpdata
	cp $(CURDIR)/backups/gamecrafts.json $(CURDIR)/gamecraft/gamecrafts/fixtures/gamecrafts.json

TAG=micktwomey/gamecraft
MOUNTS=-v /vagrant:/gamecraft/src/development:rw \
	-v /vagrant/logs:/gamecraft/logs:rw \
	-v /vagrant/uploads:/gamecraft/uploads:rw \
	-v /vagrant/backups:/gamecraft/backups:rw

all: build

build:
	docker build -t $(TAG) .

shell:
	docker run $(MOUNTS) -i -t --entrypoint=/bin/bash $(TAG) -i

migrate:
	docker run $(MOUNTS) -i -t $(TAG) migrate

runserver:
	docker run -p 8000:8000 $(MOUNTS) --name gamecraft -i -t $(TAG)

runserver-background:
	docker run -p 8000:8000 $(MOUNTS) -d --name gamecraft $(TAG)
	docker ps
	echo
	echo Use "docker stop gamecraft" to stop
	echo
	echo Use "docker attach gamecraft" to attach to the process
	echo

stop:
	docker stop gamecraft || true
	docker rm gamecraft || true

dumpdata:
	docker run -i -t $(MOUNTS) $(TAG) dumpdata --indent=2 --format=yaml --natural-foreign  --natural-primary auth.user sites.site socialaccount | grep -v RemovedInDjango18Warning > ../backups/data.yaml

loaddata:
	docker run -i -t $(MOUNTS) $(TAG) loaddata /gamecraft/backups/data.yaml

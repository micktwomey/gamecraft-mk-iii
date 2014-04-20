FROM micktwomey/python3.4:latest
MAINTAINER Michael Twomey <mick@twomeylee.name>

EXPOSE 8000

# Any config is read from here
VOLUME ["/gamecraft/config"]

# This is exposed first on the python path, so vagrant builds can use
# your checkout to run the server.
VOLUME ["/gamecraft/src/development"]

# Logs written to here
VOLUME ["/gamecraft/logs"]

# Uploaded files stored here
VOLUME ["/gamecraft/uploads"]

# Backup data into here
VOLUME ["/gamecraft/backups"]


ENV DJANGO_SETTINGS_MODULE gamecraft.settings_docker

RUN echo "deb http://ppa.launchpad.net/chris-lea/node.js/ubuntu saucy main " > /etc/apt/sources.list.d/nodejs.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7917B12

RUN apt-get -y update && \
    apt-get -y install nodejs

RUN npm install -g less@1.7.0

RUN mkdir -p /gamecraft/src
WORKDIR /gamecraft/src

ADD requirements.txt /gamecraft/src/requirements.txt
RUN pip install -r requirements.txt

# Add the dev version to the python path
RUN echo /gamecraft/src/development > /usr/local/lib/python3.4/dist-packages/gamecraft.pth

# Add the real version to the python path
RUN echo /gamecraft/src/gamecraft >> /usr/local/lib/python3.4/dist-packages/gamecraft.pth

CMD ["runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/usr/local/bin/django-admin"]

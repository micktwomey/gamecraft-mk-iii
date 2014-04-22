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

# Replace the following with the latest hash or tag, docker caches this
# so you need to use a new tag to force a rebuild.
RUN git clone --depth 1 https://github.com/micktwomey/gamecraft-mk-iii.git gamecraft && \
    cd gamecraft && \
    git checkout 2a1f5faf051231903f2413185f332caf05464a10

ADD requirements.txt /gamecraft/src/requirements.txt
RUN pip install -r requirements.txt

# Add the dev version to the python path
RUN echo /gamecraft/src/development > /usr/local/lib/python3.4/dist-packages/gamecraft.pth

# Add the real version to the python path
RUN echo /gamecraft/src/gamecraft >> /usr/local/lib/python3.4/dist-packages/gamecraft.pth

CMD ["runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/usr/local/bin/django-admin"]

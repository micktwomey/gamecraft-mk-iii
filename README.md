# GameCraft Site MK III

Written in Django. Why? Lots of plugins and docs.

Why not flask? Less plugins and seems to have stalled somewhat.

## Hosting

Free hosting with heroku, sooo much easier. If we need to scale up we can move to Digital Ocean, but that introduces deployment fu.

## Development

1. Get a Heroku account
2. Ask mick to get added to the gamecraft app
3. Install the heroku toolbox
4. heroku login
5. git remote add heroku git@heroku.com:gamecraft-it-eu.git
6. heroku fork gamecraft-it-yourname (e.g. gamecraft-it-micktwomey)
7. profit

Ok, you can also create a virtualenv and pip install -r requirements.txt, but that's no fun.

## Deployment

1. git commit
2. git push origin master

This will trigger a build on https://circleci.com/gh/micktwomey/gamecraft-mk-iii which in turn pushes to Heroku. *every push to origin/master triggers a deployment on successful test*

## Testing

1. pip3.4 install -r requirements.txt
2. python3.4 manage_development.py test --settings=gamecraft.settings

## Running the Code

If you want to run against the heroku db with your local code a neat trick is to eval the Heroku config variables.

In bash:

```sh
eval $(heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+=)(.*)/export \1"\2"/g')
```

In fish:

```sh
source (heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+)=(.*)/set -x \1 "\2"/g' | psub)
```

Running a local server against the Heroku db:
```sh
python3.4 manage.py runserver --settings gamecraft.settings_heroku_development 0.0.0.0:8000
```

### Node

You may need to do some node stuff (fish example below):

```sh
npm install less
set -lx PATH (pwd)/node_modules/less/bin $PATH
```

# Config Files

There are a few settings files:

- gamecraft.settings (base settings, use these for tests)
    + gamecraft.settings_heroku_base (core heroku settings)
        * gamecraft.settings_heroku (production heroku settings)
        * gamecraft.settings_heroku_development (local development with heroku db)
    + gamecraft.settings_local_development (local development with sqlite)

https://github.com/micktwomey/gamecraft-mk-iii/issues/2 covers getting these back into a sensible state again.

# Copying Data

To copy data from the live site to staging:
```
heroku pgbackups:transfer --app gamecraft-it-staging gamecraft-it-eu::PURPLE HEROKU_POSTGRESQL_RED
```

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
2. git push heroku master

## Testing

1. pip3.4 install -r requirements.txt
2. python3.4 manage_development.py test --settings=gamecraft.settings

## Running the Code

If you want to run against the staging db with your local code a neat trick is to eval the Heroku config variables.

In bash:

```sh
eval $(heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+=)(.*)/export \1"\2"/g')
```

In fish:

```sh
source (heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+)=(.*)/set -x \1 "\2"/g' | psub)
```

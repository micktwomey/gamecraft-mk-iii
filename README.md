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


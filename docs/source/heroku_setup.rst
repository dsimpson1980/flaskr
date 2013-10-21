Deployment to Heroku
====================

Sign up to an account on Heroku

Open a terminal and naviagate to the root of your project

Download and install the heroku toolbelt

Run $ heroku login
Enter your Heroku credentials.
Email: mapdes@gmail.com
Password (typing will be hidden):
Authentication successful.

The buildpack is located here: https://github.com/dbrgn/heroku-buildpack-python-sklearn

We're creating a new app from scratch so the command is:

    $ heroku create  --buildpack https://github.com/dbrgn/heroku-buildpack-python-sklearn/

To create the app and add it as a remote repository for git

Comment out matplotlib and pandas from requirements before pushing to heroku for first time
Add above two pkgs back in that will now use cached numpy compilation

To be able to detect what environment the app is being run on, add the following
environmental variable in heroku:

    $ heroku config:set HEROKU=1

To create the database addon:

    $ heroku add:add heroku-postgresql:dev

The initialise the database and to populate it with the structure in schema.sql

    $ heroku run init

Run the below to promote the database to DEFAULT i.e. DATABASE_URL:

    $ heroku pg:promote HEROKU_POSTGRESQL_color_URL

Promoting HEROKU_POSTGRESQL_COLOR_URL (DATABASE_URL) to DATABASE_URL... done

Run the below to start the celery worker:

    $ heroku run worker
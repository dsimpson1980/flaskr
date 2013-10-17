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

To create the database addon:

    $ heroku add:add heroku-postgresql:dev

The initialise the database:

    $ heroku run init

to populate the database with the structure in schema.sql

Run the below to promote the database to DEFAULT i.e. DATABASE_URL:

    $ heroku pg:promote HEROKU_POSTGRESQL_color_URL

Promoting HEROKU_POSTGRESQL_COLOR_URL (DATABASE_URL) to DATABASE_URL... done

Database schema structure
=========================

The postgres database has the schema structure outlined in the database below:

.. figure:: retail_schema.png
   :scale: 100%
   :alt: diagram of retail schema

   UML diagram of the retail schema in the postgres database

This structure can also be read in the schema.sql file that is used to initialise the database
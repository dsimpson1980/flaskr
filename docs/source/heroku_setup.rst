Deployment to Heroku
====================

Sign up to an account on Heroku

Open a terminal and naviagate to the root of your project

Download and install the heroku toolbelt

.. code-block:: console

	$ heroku login
	
When asked enter your Heroku login details:

.. code-block:: console

	Enter your Heroku credentials.
	Email: mapdes@gmail.com
	Password (typing will be hidden):
	Authentication successful.

The buildpack we will be using for Heroku is located here:
	
	https://github.com/dbrgn/heroku-buildpack-python-sklearn

Create a new Heroku app from scratch using this buildpack:

.. code-block:: console

    $ heroku create  --buildpack https://github.com/dbrgn/heroku-buildpack-python-sklearn/

This creates the app and adds it as a remote repository in .git/config.

The first requirements.txt file resembles the following:

.. code-block:: console

	requests
	gunicorn==0.17.2
	SQLAlchemy==0.8.2
	Flask-SQLAlchemy==1.0
	WTForms==1.0.4
	psycopg2==2.4.4
	Babel==0.9.6
	Flask-Babel==0.8
	numpy==1.7

I say the first requirements.txt file because unfortunately Heroku seems to have a problem
with precompiled cached packages in the same run.  This means that even if numpy is
compiled first it isn't available when it comes to compiling matplotlib and pandas.  First
push to Heroku:

.. code-block:: console

	$ git push heroku master
	
which should compile everything and return a successful push.  Now add the following four
lines to the requirements.txt file:

.. code-block:: console

	matplotlib==1.3.0
	pandas==0.12.0
	python-dateutil==2.1
	celery==3.0.24

and push again:

.. code-block:: console

	$ git push heroku master
	
This push will use the precompiled buildpack on heroku with the compiled numpy package.
matplotlib and pandas will now compile successfully.

To be able to detect what environment the app is being run on, add the following
environmental variable in heroku:

.. code-block:: console

    $ heroku config:set HEROKU=1

We also need to create the database addon:

.. code-block:: console

    $ heroku add:add heroku-postgresql:dev

Note: postgresql can be added for free without entering any credit card details.  However,
almost all other apps, even when using the free versions, will require you to add a credit
card.

Toi be able to run our web app we need to add a Procfile:

.. code-block:: none

	web: gunicorn run_server:app
	init: python flaskr/db_create.py
	worker: celery -A tasks worker -B --loglevel=info

This is simply a list of shortcut commands to run on the Heroku shell.  So, for instance,
to initialise the database and populate it with the structure in schema.sql you can run:

.. code-block:: console

    $ heroku run init

This will return the URL of the database in the form:

.. code-block:: console

	HEROKU_POSTGRESQL_color_URL=

We can then promote this database to DEFAULT i.e. DATABASE_URL:

.. code-block:: console

    $ heroku pg:promote HEROKU_POSTGRESQL_color_URL
	Promoting HEROKU_POSTGRESQL_COLOR_URL (DATABASE_URL) to DATABASE_URL... done

Before running a celery worker we need to add a message handler.  I've used CloudAMQP:

.. code-block:: console

	$ heroku addons:add cloudamqp:lemur
	
Note that this will fail (even though little lemur is free) with a card verification error.
So if you haven't already, you'll need to add your credit card details to Heroku.

Finally we can run the last command to start the celery worker on the Heroku remote

.. code-block:: console

    $ heroku run worker

TYPSET THIS

To run two heroku apps from the same repo we need to first create another heroku app:

.. code-block:: console

    $ heroku create

Then add a new remote repository with a suitable name e.g heroku-django

    $ code here

As we now have two apps running from the same master branch/directory we now need
to specify which app to use when running heroku commands.  The first example of
this is setting an environment variable in each app so that we can distinguish
between the two from python:

.. code-block:: console

    $ heroku config:set --app still-dawn-2729 WEB_FRAMEWORK='django'
    Setting config vars and restarting still-dawn-2729... done, v5
    WEB_FRAMEWORK: django

Then run the same for the app to be used for teh flask setup:

.. code-block:: console

    $ heroku config:set --app pacific-river-9803 WEB_FRAMEWORK='flask'
    Setting config vars and restarting pacific-river-9803... done, v29
    WEB_FRAMEWORK: flask

You can check that these environment variables have been set correctly by running
bash on the app:

.. code-block:: console

    $ heroku run --app still-dawn-2729 bash
    Running `bash` attached to terminal... up, run.8431
    ~ $ printenv
    ..
    SHLVL=2
    WEB_FRAMEWORK=django
    PYTHONPATH=/app/
    ..

We now simply need to change the contents of run_server.py to point to the
correct app for each setting of the WEB_FRAMEWORK:

.. code-block:: python

    import os
    if os.environ['WEB_FRAMEWORK'] == 'flask':
        from flask_ui import app
    if os.environ['WEB_FRAMEWORK'] is 'django':
        from django_ui import app

    if __name__ == '__main__':
        app.run(host='127.0.0.1', port=5000)

In PyCharm for local testing we can set up two configurations each with a
different setting for WEB_FRAMEWORK.  Simply follow the instructions in the
pycharm documentation covering `environmental variables`_

.. _environmental variables: http://www.jetbrains.com/pycharm/webhelp/run-debug-configuration-python.html
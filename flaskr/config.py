import os

if os.environ.get('HEROKU') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://mapdes:default@localhost/flaskr'
else:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

SQLALCHEMY_ECHO = True
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'mapdes'
PASSWORD = 'default'

#pagination
CUSTOMERS_PER_PAGE = 10
DEMAND_ITEMS_PER_PAGE = 10
PREMIUMS_PER_PAGE = 3
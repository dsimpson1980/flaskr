import os

if os.environ.get('HEROKU') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://mapdes:default@localhost/flaskr'
    CELERY_BROKER_URL = 'amqp://localhost:5672',
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    BROKER_POOL_LIMIT = 1

SQLALCHEMY_ECHO = True
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'mapdes'
PASSWORD = 'default'

#pagination
CUSTOMERS_PER_PAGE = 3
DEMAND_ITEMS_PER_PAGE = 10
PREMIUMS_PER_PAGE = 3
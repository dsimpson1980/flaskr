import sqlalchemy as sa
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config.from_object('flaskr.config')

engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)

meta = sa.MetaData(bind=engine, schema='retail')
schema = 'retail'
meta.reflect(bind=engine, schema=schema)
db = SQLAlchemy(app)

app = Flask(__name__)
app.config.update(
    #CELERY_BROKER_URL='redis://localhost:6379',
    #CELERY_RESULT_BACKEND='redis://localhost:6379'
    CELERY_BROKER_URL='amqp://localhost:5672',
    CELERY_RESULT_BACKEND='amqp://localhost:5672'
)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

import flaskr.views
#from views import Customer

celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b
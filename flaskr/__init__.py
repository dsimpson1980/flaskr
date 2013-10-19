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

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URI',
                                                       'BROKER_POOL_LIMIT'])
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
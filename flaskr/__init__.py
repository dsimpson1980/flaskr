import sqlalchemy as sa
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object('flaskr.config')

engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)

meta = sa.MetaData(bind=engine, schema='retail')
schema = 'retail'
meta.reflect(bind=engine, schema=schema)
db = SQLAlchemy(app)

import flaskr.views
from views import Customer
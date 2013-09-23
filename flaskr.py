# all the imports
import pandas as pd
import numpy as np
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
#from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Comment added on shiny thing

# postgres config
SQLALCHEMY_DATABASE_URI = "postgresql://mapdes:default@localhost/flaskr"
SQLALCHEMY_ECHO = True

# configuration
DATABASE = '/projects/pycharm/flaskr/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
# #db = SQLAlchemy(app)
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
def connect_db():
    return engine.connect()
#     sqlite approach
#     return sqlite3.connect(app.config['DATABASE'])
#
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.execute(f.read())
        db.commit()
#
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

@app.before_request
def before_request():
    # g and sqlite approach
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    # g and sqlite approach
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/retail')
def show_customers():
    # con = engine.connect()
    # cur = con.execute('SELECT customer_id, name, market FROM customers')
    # customers = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    # return render_template('show_customers.html', customers=customers)
    cur = g.db.execute('SELECT customer_id, name, market FROM retail.customers')
    customers = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    return render_template('show_customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    from StringIO import StringIO
    if not session.get('logged_in'):
        abort(401)
    # con = engine.connect()
    # con.execute('INSERT INTO retail.customers (name, market) VALUES (?, ?)',
    #              [request.form['name'], request.form['market']])
    # con.commit()
    # demand = generate_random_customer_data()
    # add push to db demand table here
    # flash('New customer was successfully added')
    # return redirect(url_for('show_customers'))
    customer_id = g.db.execute('''INSERT INTO retail.customers (name, market)
                                  VALUES (%s, %s)
                                  RETURNING customer_id''',
                               [request.form['name'], request.form['market']]).first()[0]
    # g.db.commit()
    demand = generate_random_customer_data(customer_id)
    demand_buffer = StringIO()
    demand.to_csv(demand_buffer, header=False, index=False)
    demand_buffer.seek(0)
    cur = engine.raw_connection().cursor()
    cur.copy_from(demand_buffer, 'retail.customer_demand', sep=',')
    cur.connection.commit()
    # add push to db demand table here
    flash('New customer was successfully added')
    return redirect(url_for('show_customers'))

@app.route('/display_customer/<int:customer_id>')
def display_customer(customer_id):
    if not session.get('logged_in'):
        abort(401)
    # return 'customer_id = ' + str(customer_id)
    cur = g.db.execute('SELECT customer_id, name, market FROM retail.customers WHERE customer_id = %s' % customer_id)
    customer_meta_data = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    cur = g.db.execute('SELECT datetime, value FROM retail.customer_demand WHERE customer_id =' + str(customer_id))
    customer_demand = [dict(datetime=row[0], value=row[1]) for row in cur.fetchall()]
    return render_template('display_customer.html', customer_demand=customer_demand, customer_meta_data=customer_meta_data)

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from retail.entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
    # cur = g.db.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into retail.entries (title, text) values (%s, %s)',
                 [request.form['title'], request.form['text']])
    # g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/')
def hello_world():
    return 'Hello World!'

def generate_random_customer_data(customer_id):
    """Generates some random customer data

    Dependencies
    ------------

    pandas
    numpy

    Inputs
    ------

    customer_id: int
        The customer_id associated with the demand data

    Outputs
    -------

    demand - pd.TimeSeries
        randomly generated DataFrame covering 30 days in Sep-13 at daily freq

    """
    start_date = '01-Sep-13'
    end_date = '30-Sep-13'
    dates = pd.date_range(start_date, end_date, freq='D')
    values = np.random.rand(len(dates))
    ids = np.array(range(len(dates)))
    ids.fill(customer_id)
    demand = pd.DataFrame({'customer_id': ids, 'datetime': dates, 'value': values})
    return demand


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

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

# postgres config
SQLALCHEMY_DATABASE_URI = "postgresql://mapdes:default@localhost/flaskr"
SQLALCHEMY_ECHO = True

# configuration
DATABASE = '/projects/pycharm/flaskr/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

def connect_db():
    return engine.connect()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.execute(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_customers():
    cur = g.db.execute('SELECT customer_id, name, market FROM retail.customers')
    customers = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    return render_template('show_customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    from StringIO import StringIO
    if not session.get('logged_in'):
        abort(401)
    demand = generate_random_customer_data()
    image64 = generate_customer_demand_image(demand)

    customer_id = g.db.execute('''INSERT INTO retail.customers (name, market, image64)
                                  VALUES (%s, %s, %s)
                                  RETURNING customer_id''',
                               [request.form['name'],
                                request.form['market'],
                                image64]).first()[0]
    ids = np.array(range(len(demand)))
    ids.fill(customer_id)
    demand_data = pd.DataFrame({'customer_id': ids,
                                'datetime': demand.index,
                                'value': demand.values})

    demand_buffer = StringIO()
    demand_data.to_csv(demand_buffer, header=False, index=False)
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
    cur = g.db.execute('''SELECT customer_id, name, market, image64
                          FROM retail.customers
                          WHERE customer_id = %s''' % customer_id)
    row = cur.fetchall()
    customer_meta_data = dict(customer_id=row[0][0],
                               name=row[0][1],
                               market=row[0][2],
                               image64=row[0][3])
    cur = g.db.execute('''SELECT datetime, value
                          FROM retail.customer_demand
                          WHERE customer_id =''' + str(customer_id))
    recordset = cur.fetchall()
    if recordset != []:
        dates, values = zip(*recordset)
        customer_demand = [dict(datetime=row[0], value=row[1]) for row in recordset]
        if customer_meta_data['image64'] is None:
            demand = pd.TimeSeries(values, dates)
            image64 = generate_customer_demand_image(demand)
            customer_meta_data['image64'] = image64
            cur.db.execute('SELECT')
    else:
        customer_demand = []
    return render_template('display_customer.html',
                           customer_demand=customer_demand,
                           customer_meta_data=customer_meta_data)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('''INSERT INTO retail.entries (title, text)
                    VALUES (%s, %s)''',
                 [request.form['title'], request.form['text']])
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

def generate_random_customer_data():
    """Generates some random customer data

    Dependencies
    ------------

    pandas
    numpy

    Inputs
    ------

    None

    Outputs
    -------

    demand - pd.TimeSeries
        randomly generated DataFrame covering 30 days in Sep-13 at daily freq

    """
    start_date = '01-Sep-13'
    end_date = '30-Sep-13'
    dates = pd.date_range(start_date, end_date, freq='D')
    values = np.random.rand(len(dates))
    demand = pd.TimeSeries(values, dates)
    return demand

def generate_customer_demand_image(demand):
    """Creates a plot and saves it to a string buffer

    Dependencies
    ------------
    matplotlib.pyplot
    StringIO.StringIO
    Base64

    Inputs
    ------
    demand: pandas.TimeSeries
        The historical demand for the customer

    Outputs
    -------

    image64: StringIO
        The string buffer containing the image plot


    """
    import matplotlib.pyplot as plt
    from StringIO import StringIO
    import base64

    # Extract the timeseries part from the demand dataframe

    # Plot the historical demand
    demand.plot()
    plt.xlabel('date')
    plt.ylabel('demand (kwh')
    plt.title('Historical Demand')
    plt.grid(True)

    # Store image in a string buffer and encode in base64
    buffer = StringIO()
    plt.savefig(buffer)
    plt.close()
    buffer.getvalue()
    _historical_demand_image64 = base64.b64encode(buffer.getvalue())
    return _historical_demand_image64

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

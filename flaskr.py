# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/Users/davesimpson/PycharmProjects/flaskr/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/retail')
def show_customers():
    cur = g.db.execute('SELECT customer_id, name, market FROM customers')
    customers = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    return render_template('show_customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO customers (name, market) VALUES (?, ?)',
                 [request.form['name'], request.form['market']])
    g.db.commit()
    flash('New customer was successfully added')
    return redirect(url_for('show_customers'))

@app.route('/display_customer/<int:customer_id>')
def display_customer(customer_id):
    if not session.get('logged_in'):
        abort(401)
    # return 'customer_id = ' + str(customer_id)
    cur = g.db.execute('SELECT customer_id, name, market FROM customers WHERE customer_id = ' + str(customer_id))
    customer_meta_data = [dict(customer_id=row[0], name=row[1], market=row[2]) for row in cur.fetchall()]
    cur = g.db.execute('SELECT datetime_utc, value FROM demand WHERE customer_id =' + str(customer_id))
    customer_demand = [dict(datetime_utc=row[0], value=row[1]) for row in cur.fetchall()]
    return render_template('display_customer.html', customer_demand=customer_demand, customer_meta_data=customer_meta_data)

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

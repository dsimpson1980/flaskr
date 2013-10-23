import sqlalchemy as sa
from web_ui import db, meta

class Market(db.Model):
    __tablename__ = 'markets'
    metadata = meta

class Customer(db.Model):
    __tablename__ = 'customers'
    metadata = meta

class Premium(db.Model):
    __tablename__ = 'premiums'
    metadata = meta

class CustomerDemand(db.Model):
    __tablename__ = 'customer_demand'
    metadata = meta

class Parameter(db.Model):
    __tablename__ = 'run_parameters'
    metadata = meta

class CustomerWithMarket(db.Model):
    __tablename__ = 'customer_with_market'
    __table_args__ = {'extend_existing': True,
                      'autoload': True}
    metadata = meta
    customer_id = sa.Column('customer_id',
                            sa.Integer,
                            primary_key=True)
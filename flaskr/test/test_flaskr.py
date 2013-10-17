import pandas as pd
import numpy as np
from numpy.testing import assert_raises

from .. import app, db
from .. import Customer

class TestCustomer(object):
    def test_customer_id(self):
        test_customer = Customer(name='test',
                                 market_id=1,
                                 image64=None)
        db.session.add(test_customer)
        db.session.commit()
        print test_customer.customer_id
        assert isinstance(test_customer.customer_id, int)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def check_test(self):
        assert(True)
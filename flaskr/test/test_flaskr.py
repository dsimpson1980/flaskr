import pandas as pd
import numpy as np
from numpy.testing import assert_raises

from .. import app, db

class TestCustomer(object):
    def tearDown(self):
        db.session.remove()
        db.drop_all()
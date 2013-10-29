import os
import numpy as np
from celery import Celery
from retail.views import Premium
from config import CELERY_BROKER_URL

celery = Celery('tasks', broker=CELERY_BROKER_URL)

@celery.task
def generate_premium(customer_id,
                     run_id,
                     contract_start_date,
                     contract_end_date,
                     valuation_date):
    premium = np.random.rand()
    new_premium = Premium(customer_id=customer_id,
                          run_id=run_id,
                          valuation_date=valuation_date,
                          contract_start_date_utc=contract_start_date,
                          contract_end_date_utc=contract_end_date,
                          premium=premium)
    return True

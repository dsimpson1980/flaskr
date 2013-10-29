import numpy as np
import pandas as pd

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
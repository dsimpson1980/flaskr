from django import forms
from django.forms.extras.widgets import SelectDateWidget
from wtforms import Form, validators, TextField, BooleanField
from wtforms.fields.html5 import DateField
from dateutil.relativedelta import relativedelta

class MySelectDateWidget(SelectDateWidget):
    def render(self, name, value, attrs=None):
        from collections import namedtuple
        from datetime import datetime
        start_date = datetime.today().date() + relativedelta(months=1,day=1)
        date_tweak = namedtuple('Date', 'year month day')
        date_value = date_tweak(start_date.year, start_date.month, 1) #tweak to cheat SelectDateWidget's
                                   #render method which expects a datetime object
        return super(MySelectDateWidget, self).render(name, date_value, attrs)

class ParametersForm(forms.Form):
    contract_start = forms.DateField(label="contract_start",
                                     widget=MySelectDateWidget)
    choices = [(None, '0')] + [(x, str(x)) for x in range(1,36)]
    contract_adhoc = forms.ChoiceField(label='ad hoc months', choices=choices, required=False)
    contract12 = forms.BooleanField(label="12 months", required=False, initial=True)
    contract24 = forms.BooleanField(label="24 months", required=False)
    contract36 = forms.BooleanField(label="36 months", required=False)
    email = forms.EmailField(label='email', required=False)

class AddCustomerForm(forms.Form):
    name = forms.CharField(max_length=128, label="Name")
    historical_demand = forms.FileField(label="Historical Demand")
    market = forms.ChoiceField(label='market',
                               choices=[('ukpower', 'ukpower'),
                                        ('nbp', 'nbp'),
                                        ('pegnord', 'pegnord'),
                                        ('pegsud', 'pegsud'),
                                        ('tigf', 'tigf'),
                                        ('nlpower', 'nlpower'),
                                        ('nlgas', 'nlgas')])

class premium_parameters_form(Form):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    default_start = datetime.today() + relativedelta(months=1, day=1)
    contract_start = DateField(label="contract_start",
                               default=default_start)
    #choices = [(None, '0')] + [(x, str(x)) for x in range(1,36)]
    #contract_adhoc = ChoiceField(label='ad hoc months', choices=choices, required=False)
    contract12 = BooleanField(label="12 months", default=True)
    contract24 = BooleanField(label="24 months")
    contract36 = BooleanField(label="36 months")
    email = TextField(label='Email',
                      default='mapdes@gmail.com',
                      validators=[validators.Email(message='Invalid email address')])
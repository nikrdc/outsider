from flask_wtf import Form
from wtforms import BooleanField, SubmitField

from models import prices


class FilterForm(Form):
	open_now = BooleanField('Open now')
	price_range0 = BooleanField(prices[0])
	price_range1 = BooleanField(prices[1])
	price_range2 = BooleanField(prices[2])
	price_range3 = BooleanField(prices[3])
	price_range4 = BooleanField(prices[4])
	submit = SubmitField('Filter')

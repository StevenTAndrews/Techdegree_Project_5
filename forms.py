from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

from models import Entry


def EntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    timestamp = DateField('Date (MM/DD/YYYY)', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent in Minutes', validators=[DataRequired()])
    content = TextAreaField('What you learned', validators=[DataRequired()])
    resources = TextAreaField('Resources')


def EditEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    timestamp = DateField('Date (MM/DD/YYYY)', validators=[DataRequired()])
    time_spent = IntegerField('Time Spent in Minutes', validators=[DataRequired()])
    content = TextAreaField('What you learned', validators=[DataRequired()])
    resources = TextAreaField('Resources')
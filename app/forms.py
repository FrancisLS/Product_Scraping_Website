from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired


class ProductSearchForm(FlaskForm):
    product = SearchField('What product would you like to search today?', validators=[DataRequired()])
    submit = SubmitField('Search')

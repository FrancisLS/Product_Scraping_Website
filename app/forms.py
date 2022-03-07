from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired


class ProductSearchForm(FlaskForm):
    product = SearchField('Product name', validators=[DataRequired()])
    submit = SubmitField('Search')

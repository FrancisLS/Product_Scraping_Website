from flask import render_template, flash, redirect, url_for
from app.forms import ProductSearchForm
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    user = {'username': 'Francis'}
    form = ProductSearchForm()
    if form.validate_on_submit():
        flash('Searched for {}.'.format(form.product.data))  # debug msg
        return redirect(url_for('results'))
    return render_template('home.html', title='Home', user=user, form=form)


@app.route('/results')
def results():
    return render_template('results.html', title='Search Results')

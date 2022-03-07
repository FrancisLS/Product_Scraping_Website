from flask import render_template, flash, redirect, url_for
from app.forms import ProductSearchForm
import json
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
    with open('./Amazon_Scraper/test_limited_pages.jl', 'r') as jl_file:
        json_list = list(jl_file)
    items = []
    for item in json_list:
        items.append(json.loads(item))
    return render_template('results.html', title='Search Results', items=items)

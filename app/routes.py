from app import app

import requests
from flask import render_template, flash, redirect, url_for
from app.forms import ProductSearchForm

from urllib.parse import urljoin, urlencode
import json
import pandas as pd

import scraperConfig


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    user = {'username': 'Francis'}
    form = ProductSearchForm()
    if form.validate_on_submit():
        flash('Searched for {}.'.format(form.product.data))  # debug msg
        query = form.product.data
        return results(query)
    return render_template('home.html', title='Home', user=user, form=form)


@app.route('/results', methods=['GET', 'POST'])
def results(query):
    params = {
        'spider_name': 'amazon',
        'start_requests': True,
        'crawl_args': json.dumps({'query': query})  # use json.dumps to urlencode dict as {'query': query} in URL GET
    }
    response = requests.get('http://localhost:9080/crawl.json', params)
    '''
    data = json.loads(response.text)
    data_frame = pd.DataFrame(data=data['items'],
                              columns=['asin','Title','MainImage','Rating', 'NumberOfReviews','Price','AvailableSizes',
                                       'AvailableColors','BulletPoints','SellerRank'])
    return render_template('results.html', title='Search Results',
                           tables=[data_frame.to_html(classes='data', index=False)], titles=data_frame.columns.values)
    '''
    raw_data = json.loads(response.text)
    items = raw_data['items']
    return render_template('results.html', title='Search Results', items=items)


'''
@app.route('/stubResults')
def stubResults():
    with open('./Amazon_Scraper/test_limited_pages.jl', 'r') as jl_file:
        json_list = list(jl_file)
    items = []
    for item in json_list:
        items.append(json.loads(item))
    return render_template('stubResults.html', title='Search Results', items=items)
'''

from flask import render_template
from app import app


@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'Francis'}
    return render_template('home.html', title='Home', user=user)

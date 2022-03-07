from flask import Flask
from config import Config   # Needed in WTForms

app = Flask(__name__)
app.config.from_object(Config)  # protects against CSRF in forms. Needed in WTForms.

from app import routes

import sys

sys.path.insert(0, './app/')
sys.path.insert(0, '../')
from dotenv import load_dotenv

load_dotenv('.env')

from flask import Flask
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from pg_database import SessionLocal
import exceptions as e
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CACHE_TYPE = os.environ.get("CACHE_TYPE")
    CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = os.environ.get("SECRET_KEY")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.filters['zip'] = zip

cache = Cache(app)
mail = Mail(app)
csrf = CSRFProtect().init_app(app)
from controller import *
from errors import *

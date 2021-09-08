from flask import Flask, url_for, render_template, request, redirect,flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail,Message
from datetime import datetime
import exceptions as e
import time
from werkzeug.security import check_password_hash, generate_password_hash
import string
import random
import jwt
from time import time
import qrcode
import io
import qr


class Config:
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = ""
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60*60*12
    MAIL_SERVER = ""
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""



app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['zip'] = zip

db = SQLAlchemy(app)
cache = Cache(app)
mail = Mail(app)
import mailer

from controller import *
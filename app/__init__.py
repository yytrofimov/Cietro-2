from flask import Flask, url_for, render_template, request, redirect, flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail, Message
from datetime import datetime
import exceptions as e
import time
from werkzeug.security import check_password_hash, generate_password_hash
import random
import jwt
from time import time
import qrcode
import io
import qr
from dotenv import load_dotenv
import os
import sys
from flask_wtf.csrf import CSRFProtect, CSRFError

load_dotenv('.env')


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    DEBUG_TB_ENABLED = os.environ.get("DEBUG_TB_ENABLED")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
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

db = SQLAlchemy(app)
cache = Cache(app)
mail = Mail(app)
csrf = CSRFProtect().init_app(app)
import mailer

from controller import *

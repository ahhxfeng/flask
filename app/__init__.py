#! /bin/env python
# coding=utf--8

from flask import Flask, redirect, render_template, session, flash, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager

from config import config

manager = Manager()
bootstrap = Bootstrap()
momnet = Moment()
mail = Mail()
db = SQLAlchemy()
login_m = LoginManager()
login_m.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    momnet.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_m.init_app(app)

    # main buleprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # auth buleprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app

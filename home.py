#! venv/bin/python
# coding=utf-8

import os
from datetime import datetime
from threading import Thread

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

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess "
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql://think:123456@192.168.31.60/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["FLASKY_ADMIN"] = "779107975@qq.com"
app.config["FLASKY_MAIL_SUBJECT_PREFIX"] = "[Flasky]"
app.config["FLASKY_MAIL_SENDER"] = "Flasky Admin <779107975@qq.com>"
app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("mail_username")
# app.config["MAIL_PASSWORD"] = os.getenv("mail_password")
app.config["MAIL_PASSWORD"] = "zuhhszjaokwpbefj"

manager = Manager(app=app)
bootstrap = Bootstrap(app=app)
moment = Moment(app=app)
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)
mail = Mail(app=app)


class NameForm(FlaskForm):
    name = StringField("What is your name ? ", validators=[DataRequired()])
    submit = SubmitField("sumbit")


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr(self):
        return "<User {}>".format(self.name)


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, to, templates, **kwargs):
    msg = Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"] + subject,
                  recipients=[to],
                  sender=app.config["FLASKY_MIAL_SENDER"])
    msg.body = render_template(templates + "txt", **kwargs)
    msg.html = render_template(templates + "html", **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_mail, )



@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Look like you have change your name ")
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session["known"] = False
            if app.config["FLASKY_ADMIN"]:
                send_mail("New User",
                          app.config["FLASKY_ADMIN"],
                          "mail/new_user",
                          user=user)
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    return render_template("index.html",
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get("name"),
                           known=session.get("known", False)), 200


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    manager.run()

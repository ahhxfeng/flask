#! venv/bin/python
# coding=utf-8

from datetime import datetime

from flask import Flask, redirect, render_template, session, flash, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref, dynamic_loader
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess "
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://think:123456@192.168.31.60/database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app=app)
bootstrap = Bootstrap(app=app)
moment = Moment(app=app)
db = SQLAlchemy(app=app)


class NameForm(FlaskForm):
    name = StringField("What is your name ? ", validators=[DataRequired()])
    submit = SubmitField("sumbit")


class Role(db.model):
    __tablename__ = "roles"
    id = db.Cloumn(db.Integer, primary_key=True)
    name = db.Cloumn(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(db.modle):
    __tablename__ = "users"
    id = db.Cloumn(db.Interger, primary_key=True)
    username = db.Cloumn(db.String(64), unique=True)
    role_id = db.Cloumn(db.Integer, db.Foreigenkey("roles.id"))

    def __repr(self):
        return "<User {}>".format(self.name)


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Look like you have change your name ")
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    name = session["name"]
    return render_template("index.html",
                           current_time=datetime.utcnow(),
                           form=form,
                           name=name), 200


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name), 200


@app.errorhandler(404)
def page_not_fou(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    manager.run()

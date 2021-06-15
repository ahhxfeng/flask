#! venv/bin/python
# coding=utf-8

from datetime import datetime

from flask import Flask, redirect, render_template, session, flash, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess "

manager = Manager(app=app)
bootstrap = Bootstrap(app=app)
moment = Moment(app=app)


class NameForm(FlaskForm):
    name = StringField("What is your name ? ", validators=[DataRequired()])
    submit = SubmitField("sumbit")


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

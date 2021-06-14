#! venv/bin/python
# coding=utf-8

from datetime import datetime

from flask import Flask, redirect, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
manager = Manager(app=app)
bootstrap = Bootstrap(app=app)
moment = Moment(app=app)


@app.route("/")
def index():
    return render_template("index.html", current_time=datetime.utcnow()), 200


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name), 200


@app.errorhandler(404)
def page_not_fou(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    manager.run()

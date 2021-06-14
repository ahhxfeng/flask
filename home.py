#! venv/bin/python
# coding=utf-8

from flask import Flask, redirect, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app=app)
bootstrap = Bootstrap(app=app)


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name), 200


@app.errorhandler(404)
def page_not_fou(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    manager.run()

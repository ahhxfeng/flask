#! /usr/bin/env python
# coding=utf-8

import os

from flask_script import Manager, Shell
from flask_migrate import Migrate
from .models import Role, User

from app import create_app, db

app = create_app(os.getenv("FLASKY_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("Shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

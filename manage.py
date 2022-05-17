#! venv/bin/python
# coding=utf-8
import os
from alembic.config import main

from flask_script import Manager, Shell
from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

# app = create_app(os.getenv("FLASK_CONFIG") or "default")
app = create_app("default")
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, User=User, Role=Role, db=db)


if __name__ == '__main__':
    manager.run()

#! /usr/bin/env python
# coding=utf-8

from functools import wraps
from flask import abort
from flask_login import current_user

from .models import Permission


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorator_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, kwargs)

        return decorator_func

    return decorator


def admin_required(func):
    return permission_required(Permission.ADMINISTER)(func)
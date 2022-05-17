#! /usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required, login_user

from app.email import send_email
from . import auth
from .form import LoginForm, RegisterForm
from ..models import User
from .. import db


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remmber_me.data)
            return redirect(request.args.get("next")) or url_for("main.index")
        flash("invalid username or password")

    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,
                   "Confirm your accounts",
                   "auth/mail/confirm",
                   user=user,
                   token=token)
        flash("Register success , you can login now")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash("you have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated():
        current_user.ping() 
        if not current_user.confirmed and request.endpoint[:5] != "auth" and request.endpoint != "static":
            return redirect("auth.unconfirmed")


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_annonymous() or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm")
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               "Confirm your account",
               "auth/email/confirm",
               user=current_user,
               token=token)
    flash("A new confirmation has send to your email")
    return redirect(url_for("mian.index"))

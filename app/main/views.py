#! /bin/env python
# coding=utf-8

from crypt import methods
from datetime import datetime
from os import abort, name
from urllib import request
from flask import render_template, redirect, session, url_for, current_app, flash
from flask_login import current_user, login_required
from flask_sqlalchemy.model import NameMetaMixin
from app.decorators import admin_required, permission_required

from app.email import send_email

from .. import db
from .form import EditProfileAdminForm, NameForm, EditProfileForm, PostForm
from ..models import Permission, Post, Role, User
from . import main

# @main.route("/", methods=["GET", "POST"])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.fitter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session["known"] = False
#             if current_app.config["FLASKY_ADMIN"]:
#                 send_email(current_app.config["FLASKY_ADMIN"],
#                            "New User",
#                            "mail/new_user",
#                            user=user)
#         else:
#             session["name"] = form.name.data
#             session["known"] = True
#         redirect(url_for(".index"))
#     return render_template("index.html",
#                            form=form,
#                            name=session.get("name"),
#                            known=session.get("known", False))


@main.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()

    if current_user.can(
            Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(".index")
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", form=form, posts=posts)


@main.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)


@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("You have update your profile successfuly")
        return redirect(url_for(".user", username=current_user.user(name)))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    render_template("edit-profile.html", form=form)


@main.route("/edit-profile/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("The profile has been changed success")
        return redirect(url_for(".user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("edit-profile.html", form=form, user=user)


@main.route("/follow/<username>", methods=["GET", "POST"])
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for(".index"))
    if current_user.is_follow(user):
        flash("You have already follow this user")
        return redirect(url_for(".user", username=username))
    current_user.follow(user)
    flash("You are following {0} now !".format(username))
    return redirect(url_for(".user", username=username))


@main.route("/followers/<username>", methods=["GET", "POST"])
def followers(username):
    user = User.query.filter_by(username=username)
    if user is None:
        flash("Invalid user")
        return redirect(url_for(".index"))
    page = request.args.get("page", 1, type=int)
    pagination = user.followers.paginate(
        page,
        per_page=current_app.config["Flask_FOLLOWERS_PER_PAGE"],
        error_out=False)
    follows = [{
        "user": item.follower,
        "timestamp": item.timestamp
    } for item in pagination.items]
    return render_template("follows.html",
                           user=user,
                           title="Followers of",
                           endpoint=".followers",
                           pagination=pagination,
                           follows=follows)

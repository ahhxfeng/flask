#! /usr/env pythhon
# coding=utf-8

from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms import validators
from wtforms.validators import data_required, length, email, regexp

from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField("What is your name", validators=[data_required()])
    submit = SubmitField("Submit")


class EditProfileForm(FlaskForm):
    name = StringField("Real name",
                       validators=[data_required(),
                                   length(0, 64)])
    location = StringField("Location",
                           validators=[data_required(),
                                       length(0, 64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("submit")


class EditProfileAdminForm(FlaskForm):
    email = StringField("Email",
                        validators=[data_required(),
                                    length(1, 64),
                                    email()])
    username = StringField(
        "Username",
        validators=[
            data_required(),
            length(1, 64),
            regexp("^[A-Za-z][A-Za-z0-9.]*$", 0,
                   "username must have only letters, numbers, dots")
        ])
    confirmed = BooleanField("Confirmed")
    role = SelectField("Role", coerce=int)
    name = StringField("Real name",
                       validators=[data_required(),
                                   length(1, 64)])
    location = StringField("Location",
                           validators=[data_required(),
                                       length(1, 64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.email.data != self.user.email and User.query.filter_by(
                email=field.data).first():
            raise ValidationErr("Email already registered")

    def vaildate_username(self, field):
        if field.username.data != self.user.username and User.query.filter_by(
                username=field.data).first():
            raise ValidationErr("Username already in use")


class PostForm(FlaskForm):
    body = StringField("what's on your mind now ?", validators=[data_required()])
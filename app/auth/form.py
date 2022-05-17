#! /usr/bin/env python
# coding=utf-8

from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import User


class LoginForm(FlaskForm):
    name = StringField("What is your name ?", validators=[DataRequired()])
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Length(1, 64),
                                    Email()])
    password = PasswordField("password:", validators=[DataRequired()])
    remmber_me = BooleanField()
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Length(),
                                    Email()])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$", 0,
                "Username must have only letters, numbers, dots or underscores"
            )
        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                                 EqualTo("password2",
                                         "password should be same")
                             ])
    password2 = PasswordField("Confirm Password", validators=DataRequired())
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationErr("Email already registered")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationErr("username already in use")
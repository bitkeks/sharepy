#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField(u"Username", validators=[
        DataRequired(u"Username is missing")])
    password = PasswordField(u"Password", validators=[
        DataRequired(u"Password is missing")])

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SharePy - a webapplication to share files
Created Aug 2014 by Dominik Pataky <dpa@netdecorator.org>
"""

from flask import Flask
from flask_login import LoginManager

from sharepy.database import User

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def user_loader(userid):
    return User.q.get(userid)

import frontend


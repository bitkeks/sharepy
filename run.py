#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SharePy - a webapplication to share files
Created Aug 2014 by Dominik Pataky <dpa@netdecorator.org>
"""

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return redirect(url_for('index'))


@app.route('/my/uploads')
def my_uploads():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()

#!/usr/bin/env python3
"""
Module for working with flask, flask_babel
"""
from flask import Flask, render_template
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

@app.route('/')
def index():
    return render_template("3-index.html",
                           home_title=_("home_title"),
                           home_header=_("home_header"))

if __name__ == "__main__":
    app.run()

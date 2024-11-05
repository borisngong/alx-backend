#!/usr/bin/env python3
"""
Module for working with flask, flask_babel
"""
from flask_babel import Babel
from flask import Flask, render_template


class Config:
    """
    A class responsible for Flask Babel configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)
app.url_map.strict_slashes = False


@app.route('/')
def get_index() -> str:
    """
    Represents The home page
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
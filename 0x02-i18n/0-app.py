#!/usr/bin/env python3
"""Module for working with flask_Babel """


from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class config:
    LANGUAGES = ["en", "fr"]
    # Default locale and timezone
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Making config claa as apps configuration
app.config.from_object(config)


@app.route('/')
def index():
    """ """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

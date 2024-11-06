#!/usr/bin/env python3
"""
Flask application with mock login, locale, and timezone selection.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from pytz import timezone, exceptions as pytz_exceptions
import pytz

app = Flask(__name__)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask-Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user():
    """Retrieve a user based on the login_as parameter, if provided."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set g.user for logged-in user based on the URL parameter."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    # 1. URL parameter
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # 2. User setting
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user["locale"]
    # 3. Request header
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """Determine the timezone to use."""
    # 1. URL parameter
    tz_param = request.args.get('timezone')
    if tz_param:
        try:
            return timezone(tz_param).zone
        except pytz_exceptions.UnknownTimeZoneError:
            pass

    # 2. User setting
    if g.user and g.user.get("timezone"):
        try:
            return timezone(g.user["timezone"]).zone
        except pytz_exceptions.UnknownTimeZoneError:
            pass

    # 3. Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Render the homepage with user-specific messages and timezone."""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

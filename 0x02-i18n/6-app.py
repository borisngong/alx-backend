#!/usr/bin/env python3
"""
Mock user login with priority-based locale selection
"""
from flask_babel import Babel, _
from flask import Flask, render_template, request, g


app = Flask(__name__)
babel = Babel(app)


# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Flask Babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user():
    """Retrieve a user based on the login_as parameter"""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set g.user to the logged-in user if available"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported locales."""
    # 1. Check URL parameter
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Check user settings
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user["locale"]

    # 3. Check request header
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index():
    """Render the homepage with user-specific messages"""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

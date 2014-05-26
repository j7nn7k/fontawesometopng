from __future__ import unicode_literals
from fa_generator import get_fa_image_url
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FATP_SETTINGS', silent=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/generate')
def generate():
    icon_name = validate_name(request.args.get('name'))
    icon_color = validate_color(request.args.get('color'))
    try:
        icon_size = validate_size(request.args.get('size'))
    except ValueError:
        error = 'Please enter an icon size under 1024px and only one value, please. E.g. 48. I\'ll return a squared image anyways. Thanks.'
        return '{"custom_error": "%s"}' % error, 403

    icon_url = get_fa_image_url(icon_name, icon_color, icon_size)

    if not icon_url:
        error = 'Fail, please check your input values. Got the correct Font Awesome icon name? Color: 6 digit hex value? Size under 1024px and only one value?'
        return '{"custom_error": "%s"}' % error, 404

    return '{"icon_url": "%s"}' % icon_url


def validate_name(name):
    if name:
        # TODO add proper error handling and regex
        return str(name.lower().replace('fa-', '').replace(' ', '').replace('-', '').replace('_', '').replace('#', ''))
    else:
        raise ValueError("Please provide an icon name!")


def validate_color(color):
    if color:
        # TODO add proper error handling and regex
        return str(color.lower().replace(' ', '').replace('-', '').replace('_', '').replace('#', ''))
    else:
        return '000000'


def validate_size(size):
    if size:
        return int(size.lower().replace(' ', '').replace('-', '').replace('_', '').replace('#', ''))
    else:
        return 32


if __name__ == '__main__':
    app.run()

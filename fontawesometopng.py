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
    icon_size = validate_size(request.args.get('size'))

    icon_url = get_fa_image_url(icon_name, icon_color, icon_size)

    icon_url = '{"icon_url": "%s"}' % icon_url

    return icon_url


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
        # TODO add proper error handling and regex
        return int(size.lower().replace(' ', '').replace('-', '').replace('_', '').replace('#', ''))
    else:
        return 32


if __name__ == '__main__':
    app.run()

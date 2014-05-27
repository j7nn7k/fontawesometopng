# coding=utf-8
from __future__ import unicode_literals

from fa_generator import get_fa_image_url
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify


# create our little application :)
import re

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


@app.route('/stats')
def stats():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])


@app.route('/generate')
def generate():
    errors = {}

    icon_name = request.args.get('name', None)
    icon_size = request.args.get('size', None)
    icon_color = request.args.get('color', None)

    try:
        icon_name = validate_name(icon_name)
    except ValueError as e:
        errors.update({'name': e.message})

    try:
        icon_size = validate_size(icon_size)
    except ValueError as e:
        errors.update({'size': e.message})

    try:
        icon_color = validate_color(icon_color)
    except ValueError as e:
        errors.update({'color': e.message})

    if errors:
        result = {
            'success': False,
            'errors': errors
        }
        response = jsonify(result)
        response.status_code = 400
        return response

    try:
        image_url = get_fa_image_url(icon_name, icon_color, icon_size)
    except Exception as e:
        # print e
        result = {
            'success': False,
            'exception': "Something bad occurred.\n\nLeave us a message on twitter and we will check the logs."
        }
        response = jsonify(result)
        response.status_code = 400
        return response
    else:
        result = {
            'success': True,
            'image_url': image_url
        }
        return jsonify(result)


def validate_name(name):
    if name is None or name == '':
        raise ValueError("Please provide a name of the font awesome icon you wish to download, I can't read your mind! Though my creators are working on that, I heard.")

    name = str(name).lower().replace(' ', '')

    if re.match('^([a-z-]){1,30}$', name):
        if name.startswith("fa-"):
            name = name[3:]
        return name
    else:
        raise ValueError("Please provide a valid icon name!")


def validate_color(color):
    if color is None or color == '':
        raise ValueError("Please provide a color!")

    color = str(color).replace('HASH', '#').lower().replace(' ', '')

    if re.match('^([a-z]{1,20})|(#[0-9a-f]{6})|(#[0-9a-f]{3})$', color):
        return color
    else:
        raise ValueError("Please provide a valid color!")


def validate_size(size):
    if size is None or size == '':
        raise ValueError("Please provide a size!")

    try:
        size = int(size)
    except ValueError as e:
        raise ValueError("Please provide a valid size!")

    if size < 8 or size > 1024:
        raise ValueError("Hey mate, please stay under 1024px. Working on a ラーメン (ramen) budget here ;)")

    return size


if __name__ == '__main__':
    app.run()

# coding=utf-8
from __future__ import unicode_literals
from fa_generator import get_fa_image_url, _get_icon_char
import os
import subprocess
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify


# create our little application :)
import re

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='lDJcnr2*$34lh$fgSknw?rn',
))
app.config.from_envvar('FATP_SETTINGS', silent=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/stats')
def stats():
    git_rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    path, dirs, files = os.walk("static/images").next()
    return "Git rev: {0}, No of files generated: {1}".format(git_rev, (len(files) - 1) )


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
    except ValueError as e:
        # print e
        result = {
            'success': False,
            'errors': {
                'name': e.message
            }
        }
        response = jsonify(result)
        response.status_code = 400
        return response
    except Exception as e:
        print e
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
        try:
            # just test - additional lookup inside the generator
            _get_icon_char(name)
        except ValueError as e:
            raise e
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

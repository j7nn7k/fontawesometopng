#!/usr/bin/env python
from __future__ import unicode_literals

import os.path
import re

from PIL import Image, ImageDraw, ImageFont
import tinycss


__all__ = ['_generate']


def get_fa_image_url(icon, color_hex, size):
    filename = 'images/{0}_{1}_{2}.png'.format(icon, color_hex, size)

    if os.path.isfile(filename):
        return filename

    r = int(color_hex[0:2], 16)
    g = int(color_hex[2:4], 16)
    b = int(color_hex[4:6], 16)
    color = (r, g, b)

    try:
        _generate(icon, color, size, filename)
    except Exception as e:
        print e
        return None
    else:
        return filename


def _generate(icon, color, size, filename):
    image = Image.new('RGBA', (int(size * 1.5), int(size * 1.5)), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('fontawesome-webfont.ttf', size)

    char = _get_icon_char(icon)

    draw.text((int(size * 0.25), int(size * 0.25)), char, color, font)

    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)

    bg_size = max(image.size[0], image.size[1], size)
    borderw = int((bg_size - image.size[0]) / 2)
    borderh = int((bg_size - image.size[1]) / 2)

    bg = Image.new('RGBA', (bg_size, bg_size), color=(0, 0, 0, 0))
    bg.paste(image, (borderw, borderh))
    if bg_size > size:
        bg = bg.resize((size, size))

    for i, px in enumerate(bg.getdata()):
        pixel_color = px[:3]
        if pixel_color != color:
            y = i / size
            x = i % size
            alpha = px[3]
            bg.putpixel((x, y), color + (alpha,))

    bg.save(filename)

    return True


def _get_icon_char(icon):
    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file('font-awesome.min.css')
    icon_rule = re.compile('\.fa-{0}:before,?'.format(icon))

    for rule in stylesheet.rules:
        selector = rule.selector.as_css()
        if re.search(icon_rule, selector):
            for declaration in rule.declarations:
                if declaration.name == 'content':
                    char = declaration.value.as_css()
                    char = char[1:-1]  # strip quotes
                    char = unichr(int(char[1:], 16))  # cast to int and create real unicode
                    return char
            return None


if __name__ == '__main__':
    # generate('database', 'blue', 512, "test.png")
    # generate('file-audio-o', 'red', 512, "test.png")
    # _generate('exclamation-triangle', (0, 0, 255), 512, "test2.png")
    # get_fa_image_url('exclamation-triangle', 'FF0000', 512)
    # get_fa_image_url('exclamation-triangle', 'F0F000', 512)
    get_fa_image_url('exclamation-triangle', 'FF0000', 256)


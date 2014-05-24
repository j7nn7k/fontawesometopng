#!/usr/bin/env python
from __future__ import unicode_literals

import re

from PIL import Image, ImageDraw, ImageFont
import tinycss


__all__ = ['generate']


def generate(icon, color, size, filename):
    image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('fontawesome-webfont.ttf', size)
    char = _get_icon_char(icon)
    width, height = font.getsize(char)
    x = (size - width) / 2
    y = (size - height) / 2
    pos = (x, y)
    draw.text(pos, char, color, font)
    image.save(filename)

    # bbox = image.getbbox()
    #
    # if bbox:
    #     image = image.crop(bbox)
    #
    # borderw = int((size - (bbox[2] - bbox[0])) / 2)
    # borderh = int((size - (bbox[3] - bbox[1])) / 2)
    #
    # # Create background image
    # bg = Image.new("RGBA", (size, size), (0,0,0,0))
    #
    # bg.paste(image, (borderw,borderh))
    #
    # # Save file
    # bg.save("test2.png")


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
    generate('file-audio-o', 'red', 32, "test.png")
    # generate('exclamation-triangle', 'blue', 512, "test.png")
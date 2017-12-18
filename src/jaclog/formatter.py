#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import textwrap
from time import time

from . import screen

# TODO!!!: make symbols and colors configurable

_symbols = {
    logging.ERROR: ' ',
    logging.WARNING: ' ',
    logging.INFO: ' ',
    logging.DEBUG: ' ',
    'verbose': ' ',
}

_colors = {
    logging.ERROR: ((200, 0, 0), (255, 255, 255)),
    logging.WARNING: ((255, 87, 191), (255, 255, 255)),
    logging.INFO: ((255, 224, 102), (255, 255, 255)),
    logging.DEBUG: ((64, 255, 64), (255, 255, 255)),
    'fileFuncName': ((155, 155, 155), (130, 130, 130)),
    # 'time_sep': ((130, 130, 130), (70, 70, 70)),
}


def _color_rgb(text, rgb):
  r, g, b = rgb
  return f'\033[38;2;{r};{g};{b}m{text}\033[0m'


class Formatter(logging.Formatter):

  def __init__(self, compact):
    super().__init__()
    self.compact = compact

    # (symbol + fileFuncName, relative msec since this module loaded)
    self.lastHead = ('', 0)

  def format(self, record):
    symbolColor = _colors[record.levelno]
    siteColor = _colors['fileFuncName']

    symbol = _symbols[record.levelno]
    subsystem = (record.name == '__main__') and 'main' or record.name

    head1 = _color_rgb(f'{symbol}{subsystem}', symbolColor[0])
    head2 = _color_rgb(f'[{record.filename}] {record.funcName}', siteColor[1])
    head = f'{head1} {head2}'

    message = super().format(record)

    continued = (head == self.lastHead[0])
    self.lastHead = (head, time())

    # regular relayout
    if not self.compact:
      headLine = head
      message = textwrap.indent(message, '\x20' * 2)

      if continued:
        loglines = f'\n{message}'
      else:
        loglines = f'\n{headLine}\n{message}'

    # compact layout
    else:
      '''
      logic:
        If the message is one-liner, and the screen width of the
        `f'{head} {message}` does not exceed given limit, then log out in one
        line, otherwise print headline and message line(s) in separate lines.
      '''

      oneliner = f'{head} {message}'
      if '\n' not in message and                      \
              screen.screenWidth(oneliner) <= 78 and  \
              not continued:
        loglines = oneliner
      else:
        message = textwrap.indent(message, '\x20' * 2)
        loglines = f'{head}\n{message}'

    # indent 1 space for the sake of aesthetic
    loglines = textwrap.indent(loglines, '\x20')
    return loglines

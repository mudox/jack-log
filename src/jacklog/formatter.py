#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import textwrap

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

  def __init__(self):
    super().__init__()
    self.lastHeadLine = ''

  def format(self, record):

    # head line
    color = _colors[record.levelno]
    symbol = _symbols[record.levelno]
    subsystem = (record.name == '__main__') and 'main' or record.name
    head1 = _color_rgb(f'{symbol}{subsystem}', color[0])

    color = _colors['fileFuncName']
    head2 = _color_rgb(f'[{record.filename}] {record.funcName}', color[1])

    headLine = f'{head1} {head2}'

    # body
    message = super().format(record)
    message = textwrap.indent(message, '\x20' * 2)

    # combine
    if headLine != self.lastHeadLine:
      lines = f'\n{headLine}\n{message}'
      self.lastHeadLine = headLine
    else:
      lines = f'\n{message}'

    # indent 1 space for the sake of aesthetic
    lines = textwrap.indent(lines, '\x20')
    return lines

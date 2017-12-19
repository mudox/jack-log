#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import textwrap
from datetime import timedelta
from typing import NamedTuple


class _Last(NamedTuple):
  head: str
  relativeCreated: int  # in milliseconds

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
    'delimiter': ((130, 130, 130), (70, 70, 70)),
}


def _sgrRGB(text, rgb):
  r, g, b = rgb
  return f'\033[38;2;{r};{g};{b}m{text}\033[0m'


class Formatter(logging.Formatter):

  def __init__(self, compact, interval=2000):
    super().__init__()

    self._compact = compact
    self._interval = interval

    self._last = _Last(head='', relativeCreated=0)

  def format(self, record):
    symbolColor = _colors[record.levelno]
    siteColor = _colors['fileFuncName']

    symbol = _symbols[record.levelno]
    subsystem = (record.name == '__main__') and 'main' or record.name

    head1 = _sgrRGB(f'{symbol}{subsystem}', symbolColor[0])
    head2 = _sgrRGB(f'[{record.filename}] {record.funcName}', siteColor[1])
    head = f'{head1} {head2}'

    message = super().format(record).strip()

    # continued ?
    continued = (head == self._last.head)

    # time line ?
    milliseconds = record.relativeCreated - self._last.relativeCreated
    if milliseconds > self._interval:
      timeLine = f'\x20\x20─── {timedelta(milliseconds=milliseconds)} elapsed'
      timeLine = _sgrRGB(timeLine, _colors['delimiter'][0])
    else:
      timeLine = None

    self._last = _Last(head=head, relativeCreated=record.relativeCreated)

    # regular relayout
    if not self._compact:
      headLine = head
      message = textwrap.indent(message, '\x20' * 2)

      if continued:
        if timeLine is not None:
          loglines = f'\n{timeLine}\n\n{message}'
        else:
          loglines = f'\n{message}'
      else:
        if timeLine is not None:
          loglines = f'\n{timeLine}\n\n{headLine}\n{message}'
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

      message = textwrap.indent(message, '\x20' * 2)
      if continued:
        message = _sgrRGB('·\x20', _colors['delimiter'][0]) + message[2:]
        loglines = message
      else:
        loglines = f'{head}\n{message}'

    # indent 1 space for the sake of aesthetic
    loglines = textwrap.indent(loglines, '\x20')
    return loglines

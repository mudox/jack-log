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
    self._msgIndent = 1
    self._bodyIndent = 2

  def format(self, record):
    self._record = record

    # self._head
    symbolColor = _colors[record.levelno]
    siteColor = _colors['fileFuncName']

    symbol = _symbols[record.levelno]
    subsystem = (record.name == '__main__') and 'main' or record.name

    head1 = _sgrRGB(f'{symbol}{subsystem}', symbolColor[0])
    head2 = _sgrRGB(f'[{record.filename}] {record.funcName}', siteColor[1])
    self._head = f'{head1} {head2}'

    # self._message
    self._message = super().format(record).strip()

    # self._inOneLine
    if self._message.startswith('o:'):
      self._inOneLine = True
      self._message = self._message[2:]
    else:
      self._inOneLine = False

    # format
    if not self._compact:
      lines = self._formatRegularly()
    else:
      lines = self._formatCompactly()

    self._last = _Last(
        head=self._head,
        relativeCreated=record.relativeCreated
    )

    # indent 1 space for the sake of aesthetic
    lines = textwrap.indent(lines, '\x20' * self._msgIndent)
    return lines

  def _formatRegularly(self):
    headLine = self._head
    message = textwrap.indent(self._message, '\x20' * self._bodyIndent)

    if self._head == self._last.head:
      if self._timeLine is not None:
        lines = f'\n{self._timeLine}\n\n{message}'
      else:
        lines = f'\n{message}'
    else:
      if self._timeLine is not None:
        lines = f'\n{self._timeLine}\n\n{headLine}\n{message}'
      else:
        lines = f'\n{headLine}\n{message}'

    return lines

  def _formatCompactly(self):
    message = textwrap.indent(self._message, '\x20' * self._bodyIndent)

    if self._inOneLine:
      lines = f'{self._head}{message[self._bodyIndent:]}'
    else:
      if self._head == self._last.head:
        # continue line symbol
        message = _sgrRGB('·\x20', _colors['delimiter'][0]) + message[2:]
        lines = message
      else:
        lines = f'{self._head}\n{message}'

    return lines

  def _timeLine(self):
    # time line ?
    milliseconds = self._record.relativeCreated - self._last.relativeCreated
    if milliseconds > self._interval:
      timeLine = f'\x20\x20─── {timedelta(milliseconds=milliseconds)} elapsed'
      timeLine = _sgrRGB(timeLine, _colors['delimiter'][0])
    else:
      timeLine = None

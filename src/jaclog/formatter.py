# -*- coding: utf-8 -*-

import logging
import textwrap
from datetime import datetime, timedelta
from typing import NamedTuple
import re

from . import screen
from .settings import settings as cfg


class _Last(NamedTuple):
  subsystem: str
  fileFunc: str
  relativeCreated: int  # in milliseconds


_mlinePattern = re.compile(r'^m:\n(.*)\n[ \t]*$', re.DOTALL)


class Formatter(logging.Formatter):

  def __init__(self, compact=True, interval=2000):
    super().__init__()

    self._compact = compact
    self._interval = interval

    self._last = _Last(subsystem='', fileFunc='', relativeCreated=0)

  def _symbol(self):
    return cfg.symbols[self._record.levelname.lower()]

  def _continuedSymbol(self):
    return cfg.symbols[self._record.levelname.lower() + '+']

  def _symbolColor(self):
    return cfg.colors[self._record.levelname.lower()]

  def _subsystem(self):
    if self._record.name == '__main__':
      return 'main'
    else:
      return self._record.name

  def _fileFunc(self):
    return f'[{self._record.filename}] {self._record.funcName}'

  def format(self, record):
    self._record = record

    self._isContinued = \
        self._subsystem() == self._last.subsystem and \
        self._fileFunc() == self._last.fileFunc

    # self._head
    head1 = self._symbol().ljust(cfg.symbolWidth)
    head1 += self._subsystem()
    head1 = screen.sgr(head1, self._symbolColor())

    head2 = self._fileFunc()
    head2 = screen.sgr(head2, cfg.colors['file'])

    self._head = f'{head1} {head2}'

    # self._message
    self._message = super().format(record)

    # handle `m:` prefix
    self._mline()

    # handle `o:` prefix
    # set result into self._inOneLine
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
        subsystem=self._subsystem(),
        fileFunc=self._fileFunc(),
        relativeCreated=record.relativeCreated)

    # indent 1 space for the sake of aesthetic
    lines = textwrap.indent(lines, '\x20' * cfg.margin)
    return lines

  def _formatRegularly(self):
    headLine = self._head
    message = textwrap.indent(self._message, '\x20' * cfg.symbolWidth)

    timeLine = self._timeLine()

    if self._isContinued:
      if timeLine is not None:
        lines = f'\n{timeLine}\n\n{message}'
      else:
        lines = f'\n{message}'
    else:
      if timeLine is not None:
        lines = f'\n{timeLine}\n\n{headLine}\n{message}'
      else:
        lines = f'\n{headLine}\n{message}'

    return lines

  def _formatCompactly(self):
    message = textwrap.indent(self._message, '\x20' * cfg.symbolWidth)

    if self._inOneLine:
      lines = f'{self._head}\x20{message[cfg.symbolWidth:]}'
    else:
      if self._isContinued:
        message = screen.sgr(f'{self._continuedSymbol()}\x20',
                             self._symbolColor()) + message[2:]
        lines = message
      else:
        lines = f'{self._head}\n{message}'

    timeLine = self._timeLine()
    if timeLine is not None:
      lines = f'{timeLine}\n{lines}'

    return lines

  def _timeLine(self):
    milliseconds = self._record.relativeCreated - self._last.relativeCreated

    if milliseconds > self._interval:
      timeLine = "\x20" * cfg.symbolWidth
      timeLine += f'\n {datetime.now()} ── {timedelta(milliseconds=milliseconds)} elapsed'
      timeLine = screen.sgr(timeLine, cfg.colors['time'])

      padding = []
      for _ in range(cfg.logTimeLinePadding):
        padding += ''

      lines = padding + [timeLine] + padding
      return '\n'.join(lines)

    else:
      timeLine = None

  def _mline(self):
    m = _mlinePattern.match(self._message)
    if m is not None:
      self._message = textwrap.dedent(m.group(1))

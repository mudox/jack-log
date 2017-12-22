#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from os.path import getmtime
from pathlib import Path
from time import time

from .formatter import Formatter

__version__ = '1.0.0'


def configure(
    appName,
    fileName=None,
    logTTY=None,
    compact=True,
    eventInterval=2000,
    sessionInterval=5,
    wrap=None
):
  """ Configure logging system.

  Arguments:

    appName (str): jacklog will create f"~/.local/share/{appName}/log"
      automaticall,

    fileName (str): the name of log file that will be created, defaults to
      `{appName}.log`

    tty (Path or str): specified tty file to log directly to the corresponding
      terminal.

    compact (bool): compact relayout mode, less separating empty lines,
      defaults to False.

    eventInterval (int): time limit to add a time line in milliseconds.
      default to 2s.

    sessionInterval (int): time limit to add a session time line in seconds,
      defaults to 5s.

    wrap (int): textwrap maximum width, default to not wrap text.
  """

  if fileName is None:
    fileName = f'{appName}.log'

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.NOTSET)

  # log to file
  logFile = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()
  logFile.parent.mkdir(parents=True, exist_ok=True)
  if not logFile.exists():  # avoid change mtime if file exists
    logFile.touch(exist_ok=True)

  logToFile = logging.FileHandler(logFile)
  logToFile.setFormatter(Formatter(compact, eventInterval))
  rootLogger.addHandler(logToFile)

  # log to tty if any
  if logTTY is not None:
    logToTTY = logging.FileHandler(logTTY)
    logToTTY.setFormatter(Formatter(compact, eventInterval))
    rootLogger.addHandler(logToTTY)

  _logSessionLine(logFile, logTTY, interval=sessionInterval, compact=compact)


def _logSessionLine(logFile, tty, interval, compact):
  lines = f'\x20{datetime.now()}\x20'.center(100, '·')
  lines = f'{lines}\n' if compact else f'\n\n{lines}\n\n'

  # time separator
  modifiedTime = getmtime(logFile)
  seconds = time() - modifiedTime
  if seconds > interval:
    timeLine = f'{timedelta(seconds=seconds)} elapsed'
    timeLine = timeLine.center(100)
    timeLine = f'\n{timeLine}\n\n'

    lines = f'{timeLine}{lines}'

  lines = f'\x1b[38;5;242m{lines}\x1b[0m'
  with logFile.open('a') as file:
    file.write(lines)

  if tty is not None:
    if isinstance(tty, Path):
      with tty.open('a') as file:
        file.write(lines)
    elif isinstance(tty, str):
      with open(tty, 'a') as file:
        file.write(lines)
    else:
      raise RuntimeError(
          'argument `tty` must be either of type `Path` or `str`')

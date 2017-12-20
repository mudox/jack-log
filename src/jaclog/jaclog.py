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
    appName: 'jacklog will create f"~/.local/share/{appName}/log" automaticall',
    fileName: 'the name of log file that will be created',
    logTTY: 'specified tty file to log directly to the corresponding terminal' = None,
    compact: 'compact relayout mode, less separating empty lines' = False,
    eventInterval: 'time limit to add a time line in milliseconds. (default 2s)' = 2000,
    sessionInterval: 'time limit to add a session time line in seconds' = 5
):

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
    with tty.open('a') as file:
      file.write(lines)

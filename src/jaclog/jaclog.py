#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
from pathlib import Path

from .formatter import Formatter

__version__ = '1.0.0'


def configure(
    appName: 'jacklog will create f"~/.local/share/{appName}/log" automaticall',
    fileName: 'the name of log file that will be created',
    logTTY: 'specified tty file to log directly to the corresponding terminal' = None,
    compact: 'compact relayout mode, less separating empty lines' = False,
    interval: 'time limit to add a time line in milliseconds. (default 2s)' = 2000
):
  lines = f'------------ {datetime.datetime.now()} ------------'
  lines = f'\n{lines}\n' if compact else f'\n\n{lines}\n\n'

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.NOTSET)

  # log to file
  logFile = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()
  logFile.parent.mkdir(parents=True, exist_ok=True)

  logToFile = logging.FileHandler(logFile)
  logToFile.setFormatter(Formatter(compact, interval))
  rootLogger.addHandler(logToFile)

  with logFile.open('a') as file:
    file.write(lines)

  # log to tty if any
  if logTTY is not None:
    logToTTY = logging.FileHandler(logTTY)
    logToTTY.setFormatter(Formatter(compact, interval))
    rootLogger.addHandler(logToTTY)

    with open(logTTY, 'w') as file:
      file.write(lines)

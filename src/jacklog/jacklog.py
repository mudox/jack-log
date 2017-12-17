#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
from pathlib import Path

from .formatter import Formatter

__version__ = '1.0.0'


def configure(appName, fileName, logTTY=None):
  lines = f'------------ {datetime.datetime.now()} ------------'
  lines = f'\n\n\n{lines}\n\n\n'

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.NOTSET)

  # log to file
  logFile = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()
  logFile.parent.mkdir(parents=True, exist_ok=True)

  logToFile = logging.FileHandler(logFile)
  logToFile.setFormatter(Formatter())
  rootLogger.addHandler(logToFile)

  with logFile.open('a') as file:
    file.write(lines)

  # log to tty if any
  if logTTY is not None:
    logToTTY = logging.FileHandler(logTTY)
    logToTTY.setFormatter(Formatter())
    rootLogger.addHandler(logToTTY)

    with open(logTTY, 'w') as file:
      file.write(lines)

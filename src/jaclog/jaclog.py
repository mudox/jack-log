# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from os.path import basename, getmtime
from pathlib import Path
from sys import argv
from time import time

from .formatter import Formatter
from .screen import sgr
from .settings import settings as cfg

__version__ = '1.1'


handlers = []


def configure(
    *,
    compact=True,
    eventInterval=2000,
    sessionInterval=5,
    printSessionLine=True,
    **kargs,
):
  """ Configure logging system.

  Arguments:

    appName (str): jacklog will create f"~/.local/share/{appName}/log"
      automaticall,

    fileName (str): the name of log file that will be created, defaults to
      `{appName}.log`

    extraFiles: (list): list of paths of other log files, e.g. tty path.

    compact (bool): compact relayout mode, less separating empty lines,
      defaults to False.

    eventInterval (int): time limit to add a time line in milliseconds.
      default to 2s.

    sessionInterval (int): time limit to add a session time line in seconds,
      defaults to 5s.

    wrap (int): textwrap maximum width, default to not wrap text.

  Return: All configured log files as path str in a list.
  """

  appName = kargs.get('appName', None)
  fileName = kargs.get('fileName', None)
  extraFiles = kargs.get('extraFiles', [])

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.NOTSET)
  for h in handlers:
    rootLogger.removeHandler(h)

  # log to file
  if appName is not None:

    if fileName is None:
      fileName = f'{appName}.log'

    logFile = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()

    logFile.parent.mkdir(parents=True, exist_ok=True)
    if not logFile.exists():  # avoid change mtime if file exists
      logFile.touch(exist_ok=True)

    handler = logging.FileHandler(logFile)
    handler.setFormatter(Formatter(compact, eventInterval))
    rootLogger.addHandler(handler)
    handlers.append(handler)

  for p in extraFiles:
    filePath = Path(str(p)).expanduser()

    filePath.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(filePath)
    handler.setFormatter(Formatter(compact, eventInterval))
    rootLogger.addHandler(handler)
    handlers.append(handler)

  if printSessionLine:
    _logSessionLine(
        [logFile] + extraFiles,
        interval=sessionInterval,
        compact=compact)


def _sessionTimeLine(logFile, interval):
  # time separator
  mtime = getmtime(logFile)
  seconds = time() - mtime

  if seconds > interval:
    indent = cfg.margin + cfg.symbolWidth
    timeLine = ('·' * indent) + f'[ {timedelta(seconds=seconds)} ]'
    timeLine = sgr(timeLine, cfg.colors['time'])
    timeLine = f'{timeLine}'

    padding = []
    for _ in range(cfg.sessionTimeLinePadding):
      padding.append('')

    lines = padding + [timeLine] + padding
    return '\n'.join(lines)

  else:
    return None


def _logSessionLine(files, interval, compact):
  launchSymbol = f'{cfg.symbols["launch"]:{cfg.symbolWidth}}'
  launchSymbol = sgr(launchSymbol, cfg.colors['launch'])

  timestamp = sgr(str(datetime.now()), cfg.colors['time'])

  cmd = basename('\x20'.join(argv))
  cmd = sgr(cmd, cfg.colors['launch'])

  launchLine = f'\x20{launchSymbol}{timestamp} {cmd}'
  launchLine = f'\n{launchLine}\n\n' if compact else f'\n\n{launchLine}\n\n'

  timeLine = _sessionTimeLine(files[0], interval)
  launchLine = f'{timeLine or ""}{launchLine}'

  launchLine = f'\x1b[38;5;242m{launchLine}\x1b[0m'

  for f in files:
    with open(f, 'a') as file:
      file.write(launchLine)

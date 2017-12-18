#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from jaclog.jaclog import configure


def main_test():
  appName = 'test_jaclog'
  fileName = 'test.log'

  p = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()

  configure(appName, fileName)
  assert p.exists()

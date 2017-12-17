#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from jacklog.jacklog import configure


def test_configure():
  appName = 'test_jacklog'
  fileName = 'test.log'

  p = Path(f'~/.local/share/{appName}/log/{fileName}').expanduser()

  configure(appName, fileName)
  assert p.exists()

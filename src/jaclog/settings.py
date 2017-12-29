# -*- coding: utf-8 -*-

from pathlib import Path

from ruamel.yaml import YAML

from .screen import color2sgr


def _get(d, *paths):
  """ Query into configuration dictionary, return None on any error
  usag:
    _get(d, 'k1.2.k3.k4', 2, 'name')
  """
  if d is None:
    return None

  if paths is None:
    return None

  for path in paths:
    if path is None:
      return None

    path = path.split('.')
    for key in path:
      try:
        i = int(key)
        if i in d:
          return d[i]
        else:
          return None

      except BaseException:
        d = d.get(key, None)
        if d is None:
          return None

  return d


class _Settings:

  def __init__(self):
    self._loadConfigs()
    self._loadSymbols()
    self._loadColors()

    # margin
    v, d = self._valueAt('margin')
    if isinstance(v, int) and v > 0:
      self.margin = v
    else:
      self.margin = d

    # symbolWidth
    v, d = self._valueAt('symbols.width')
    if isinstance(v, int) and v > 0:
      self.symbolWidth = v
    else:
      self.symbolWidth = d

    # sessionTimeLinePadding
    v, d = self._valueAt('sessionTimeLinePadding')
    if isinstance(v, int) and v > 0:
      self.sessionTimeLinePadding = v
    else:
      self.sessionTimeLinePadding = d

    # logTimeLinePadding
    v, d = self._valueAt('logTimeLinePadding')
    if isinstance(v, int) and v > 0:
      self.logTimeLinePadding = v
    else:
      self.logTimeLinePadding = d

  def _valueAt(self, *paths):
    u = _get(self.userConfig, *paths)
    d = _get(self.defaultConfig, *paths)
    return u, d

  def _loadConfigs(self):
    yaml = YAML()

    defaultFile = Path(__file__).parent / 'resources' / 'jaclog.yml'
    self.defaultConfig = yaml.load(defaultFile)

    userFile = Path('~/.config/jaclog/jaclog.yml').expanduser()
    userFile.parent.mkdir(parents=True, exist_ok=True)
    if not userFile.exists():
      userFile.write_text(defaultFile.read_text())
    self.userConfig = yaml.load(userFile)

  def _loadSymbols(self):
    use = _get(self.userConfig, 'symbols.use')
    scheme = _get(self.userConfig, 'symbols.schemes', use)
    default = _get(self.defaultConfig, 'symbols.schemes.default')

    symbols = {}
    for name in default:
      v = _get(scheme, name)
      d = default[name]

      if isinstance(v, str):
        symbols[name] = v[0]
      else:
        symbols[name] = d

    self.symbols = symbols

  def _loadColors(self):
    # colors
    use = _get(self.userConfig, 'colors.use')
    scheme = _get(self.userConfig, 'colors.schemes', use)
    default = _get(self.defaultConfig, 'colors.schemes.default')

    colors = {}
    for name in default:
      colors[name] = color2sgr(_get(scheme, name)) \
          or color2sgr(default[name])

    self.colors = colors


settings = _Settings()

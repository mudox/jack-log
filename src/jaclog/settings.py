# -*- coding: utf-8 -*-


from pathlib import Path

from ruamel.yaml import YAML

from .screen import color2sgr


def _get(d, *keyss):
  if d is None:
    return None

  if keyss is None:
    return None

  for keys in keyss:
    if keys is None:
      return None

    keys = keys.split('.')
    for key in keys:
      d = d.get(key, None)
      if d is None:
        return None

  return d


# config data
_yaml = YAML()

_path = Path('~/.config/jaclog/jaclog.yml').expanduser()
_path.parent.mkdir(parents=True, exist_ok=True)
configData = _yaml.load(_path)

_path = Path(__file__).parent / 'resources' / 'jaclog.yml'
defaultConfigData = _yaml.load(_path)

del _path
del _yaml

# symbols

_use = _get(configData, 'symbols.use')
_scheme = _get(configData, 'symbols.schemes', _use)
_default = _get(defaultConfigData, 'symbols.schemes.nerd')

symbolWidth = _get(configData, 'symbols.symbolWidth') \
    or _get(defaultConfigData, 'symbols.symbolWidth')

symbols = {}
for name in _default:
  symbols[name] = _get(_scheme, name) \
      or _default[name]

# colors
_use = _get(configData, 'colors.use')
_scheme = _get(configData, 'colors.schemes', _use)
_default = _get(defaultConfigData, 'colors.schemes.basic')

colors = {}
for name in _default:
  colors[name] = color2sgr(_get(_scheme, name)) \
      or color2sgr(_default[name])

del _use
del _scheme
del _default

# margins

margin = 1

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random

from faker import Faker

from jaclog import jaclog

jaclog.configure(appName='test_jaclog', fileName='test.log', compact=True)
faker = Faker()

lastLogFunction = logger = logging.getLogger(__name__).info
lastLogFunction('this is jaclog test utiity')

try:
  while True:
    subsystem = '.'.join(faker.words(nb=random.randrange(1, 4)))
    logger = logging.getLogger(subsystem)

    logFunctions = [logger.error, logger.warning, logger.info, logger.debug]
    log = random.choice(logFunctions)

    lineCount = random.randrange(1, 4)
    lines = ''
    for _ in range(lineCount):
      lines += '\n' + faker.sentence(nb_words=7)
    lines = lines.strip()
    kind = input('kind of message content [c|o|mo|co|cmo]:')

    print(f'>> org lines:\n{lines}')

    if kind == 'o':
      lines = 'o:  🦁  [o]'
      continued = False

    elif kind == 'mo':
      lines = f'o:  🐸  [mo]\n{lines}'
      continued = False

    if kind == 'co':
      lines = 'o:  🐵  [co]'
      continued = True

    elif kind == 'cmo':
      lines = f'o:  🐼  [cmo]\n{lines}'
      continued = True

    elif kind == 'c':
      continued = True

    else:
      continued = False

    dice = random.choices(
        ['bare one liner', 'multiline one liner', 'normal'],
        weights=[2, 5, 7]
    )[0]

    print(f'>> lines:\n{lines}')

    if continued:
      log = lastLogFunction

    log(lines)
    lastLogFunction = log

except KeyboardInterrupt:
  exit(0)

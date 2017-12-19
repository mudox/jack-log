#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
from time import sleep

from faker import Faker
from jaclog import jaclog

jaclog.configure(appName='test_jaclog', fileName='test.log', compact=True)
faker = Faker()

lastLogFunction = None
while True:
  sleep(random.randrange(0, 19) / 10)

  subsystem = '.'.join(faker.words(nb=random.randrange(1, 4)))
  logger = logging.getLogger(subsystem)

  logFunctions = [logger.error, logger.warning, logger.info, logger.debug]
  log = random.choice(logFunctions)

  lineCount = random.randrange(1, 5)
  lines = ''
  for _ in range(lineCount):
    lines += '\n' + faker.sentence(nb_words=7)

  if random.randrange(4) == 0 and lastLogFunction is not None:
    lastLogFunction(lines)
  else:
    lastLogFunction = log
    log(lines)


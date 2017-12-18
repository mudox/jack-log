#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
from time import sleep

from faker import Faker
from jaclog import jaclog

jaclog.configure(appName='test_jaclog', fileName='test.log', compact=False)
faker = Faker()

while True:
  sleep(random.randrange(0, 37) / 10)

  subsystem = '.'.join(faker.words(nb=random.randrange(1, 4)))
  logger = logging.getLogger(subsystem)

  logFunctions = [logger.error, logger.warning, logger.info, logger.debug]
  log = random.choice(logFunctions)

  lineCount = random.randrange(1, 5)
  lines = ''
  for _ in range(lineCount):
    lines += '\n' + faker.sentence(nb_words=7)

  log(lines)

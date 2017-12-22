# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re

from setuptools import find_packages, setup

version = re.search(
    r"^__version__\s*=\s*'(.*)'",
    open('src/jaclog/jaclog.py').read(),
    re.M
).group(1)


setup(
    name='jaclog',
    version=version,

    description='TBD',
    long_description='TBD',

    author='Mudox',
    author_email='imudox@gmail.com',
    url='https://github.com/mudox/jaclog'

    package_dir={'': 'src'},
    packages=find_packages('src'),

    package_data={
        '': ['resources/*'],
    },
)

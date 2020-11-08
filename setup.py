#!/usr/bin/env python3
"""
Argslib
=======

A library for parsing command line arguments.

"""

import os
import re
import io

from setuptools import setup


metapath = os.path.join(os.path.dirname(__file__), 'argslib.py')
with io.open(metapath, encoding='utf-8') as metafile:
    regex = r'''^__([a-z]+)__ = ["'](.*)["']'''
    meta = dict(re.findall(regex, metafile.read(), flags=re.MULTILINE))


setup(
    name = 'argslib',
    version = meta['version'],
    py_modules = ['argslib'],
    author = 'Darren Mulholland',
    url = 'https://github.com/dmulholl/argslib',
    license = 'Public Domain',
    description = (
        'A minimalist argument-parsing library.'
    ),
    long_description = __doc__,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Public Domain',
    ],
)

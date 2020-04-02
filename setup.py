#!/usr/bin/env python3
"""
Janus
=====

Janus is a minimalist argument-parsing library designed for building elegant command-line interfaces.

Install::

    $ pip install libjanus

Import::

    >>> import janus

See the project's `documentation <http://www.dmulholl.com/docs/janus/>`_
for further details.

"""

import os
import re
import io

from setuptools import setup


filepath = os.path.join(os.path.dirname(__file__), 'janus.py')
with io.open(filepath, encoding='utf-8') as metafile:
    regex = r'''^__([a-z]+)__ = ["'](.*)["']'''
    meta = dict(re.findall(regex, metafile.read(), flags=re.MULTILINE))


setup(
    name = 'libjanus',
    version = meta['version'],
    py_modules = ['janus'],
    author = 'Darren Mulholland',
    url = 'https://github.com/dmulholl/janus',
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

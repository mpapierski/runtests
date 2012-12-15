#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
	name='runtests',author='',author_email='',
	packages=['runtests',],
	entry_points={
        'console_scripts': [
            'runtests = runtests.cli:main',
        ],
    },
    install_requires=['PyYAML',],
)
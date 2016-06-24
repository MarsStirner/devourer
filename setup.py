#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='devourer',
    version='0.1.0',
    url='https://stash.bars-open.ru/scm/medvtr/devourer.git',
    author='hitsl',
    description='MIS file storage system',
    long_description=read('README.md'),
    include_package_data=True,
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Fanstatic',
        'Flask-SQLAlchemy',
        'tsukino_usagi',
        'hitsl_utils',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

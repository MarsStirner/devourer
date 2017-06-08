#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('devourer/static')
extra_files.extend(package_files('devourer/templates'))

setup(
    name='devourer',
    version='0.1.3',
    url='https://stash.bars-open.ru/scm/medvtr/devourer.git',
    author='hitsl',
    description='MIS file storage system',
    long_description=read('README.md'),
    include_package_data=True,
    packages=find_packages(),
    package_data={
        '': extra_files
    },
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Cors',
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

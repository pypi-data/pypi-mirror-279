#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from setuptools import setup as __setup__, find_packages

def setup(install_requires=[]):
    __setup__(
        name=environ.get('MODULE_NAME'),
        install_requires=install_requires,
        packages=find_packages(),
    )

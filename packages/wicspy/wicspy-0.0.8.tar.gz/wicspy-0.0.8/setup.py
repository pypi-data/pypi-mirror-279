#!python
# -*- coding:utf-8 -*-

'''
Author: wicsp wicspa@gmail.com
Date: 2024-06-05 13:45:00
LastEditors: wicsp wicspa@gmail.com
LastEditTime: 2024-06-06 16:19:43
FilePath: /wicspy/setup.py
Description: 

Copyright (c) 2024 by wicsp, Licensed under the MIT license.
'''

from __future__ import print_function
from setuptools import setup, find_packages
import wicspy

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="wicspy",
    version=wicspy.__version__,
    author="wicsp",
    author_email="wicspa@gmail.com",
    description="A Python package for wicsp.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/wicsp/wicspy",
    py_modules=['wicspy'],
    install_requires=['loguru', 'requests', 'tqdm'],
    packages=find_packages(),
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

#!usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 KiryxaTech
"""

version = "0.0.7"

with open('README.md', encoding='utf-8') as f:
    long_discription = f.read()

setup(
    name='JsonStructor',
    version=version,

    author='KiryxaTech',
    author_email='kiryxatech@gmail.com',

    description=(u'The `JsonStructor` library is a Python package that simplifies the process '
                 u'of working with JSON files. It offers a user-friendly interface for '
                 u'reading, writing, and editing JSON data, making it easy to add, remove, '
                 u'or alter key-value pairs in a JSON file. Ideal for developers who need '
                 u'to interact with JSON data in their applications, `JsonStructor` streamlines '
                 u'common JSON operations with its straightforward and intuitive methods.'),
    long_description=long_discription,
    long_description_content_type='text/markdown',

    url='https://github.com/KiryxaTechDev/JsonStructor',
    download_url=f'https://github.com/KiryxaTechDev/JsonStructor/archive/refs/tags/{version}.zip',

    packages=['JsonStructor'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)
#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='collector_test',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'collector_test=collector_test.collector_test:main',
        ],
    },
    package_data={
        '': ['../build_number.txt',
             'customerdata/*/*.yaml',
             'customerdata/*.yaml',
        ]
    },
    install_requires=['docopt', 'splinter', 'requests'],
    author='Volker Haas',
    author_email='volker.haas@pediapress.com',
    description='Collector Test',
)

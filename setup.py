#!/usr/bin/env python

from setuptools import setup

from action_statistics import __version__

setup(
    name='ActionStatistics',
    version=__version__,
    author='Ryan Steele',
    author_email='imacube@gmail.com',
    packages=[
        'action_statistics'
    ],
    install_requires=[],
    scripts=[],
    url='http://github.com/imacube/action_statistics',
    license='LICENSE',
    description='Concurrency safe library to store actions with their respective times and return the average for each action.',
    long_description=open('README.md').read() + '\n\n' +
                     open('CHANGES.md').read()
)

#!/usr/bin/env python

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pypremiumsim',
    version='0.0.0',
    description="PremiumSIM API (Unofficial). Access basic account details and status information.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='PremiumSIM mobile phone handy balance status web germany deutschland scraper api',
    author='Jack Higgins',
    author_email='pypi@jackhiggins.ie',
    url='https://github.com/skhg/pyPremiumSIM',
    packages=['pypremiumsim'],
    install_requires=[
        'requests',
        'bs4'
    ],
    tests_require=[
        'mock',
        'nose',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'])

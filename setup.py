#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'TracDuplicates',
    version = '0.11',
    packages = ['tracduplicates'],
    author = "Nils Maier",
    author_email = "testnutzer123@gmail.com",
    description = "Provides support for duplicates ticket references",
    license = "BSD",
    keywords = "trac plugin ticket dependencies duplicates",
    url = "http://tn123.ath.cx/TracDuplicates",
    classifiers = [
        'Framework :: Trac',
    ],
    
    entry_points = {
        'trac.plugins': [
            'tracduplicates.web_ui = tracduplicates.web_ui',
        ]
    }
)

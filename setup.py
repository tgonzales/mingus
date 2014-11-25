#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name = 'mingus-rest-framework',
    version = __version__,
    description = "Mingus is a small and flexible  restful framework on top of "\
            "Tornado. It provides a simpler way to create RESTful API's.",
    long_description = """
        Mingus is a small and flexible  restful framework on top of 
            "Tornado. It provides a simpler way to create RESTful API's.
    """,
    keywords = ['restful', 'rest', 'api', 'tornado', 'motor'],
    author = 'github.com/tgonzales',
    author_email = 'dev.cleiton.couto@gmail.com',
    url = 'https://github.com/tgonzales/mingus',
    download_url = 'https://github.com/tgonzales/mingus/archive/v0.1.tar.gz',
    license = 'MIT',
    classifiers = [
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
      "tornado>=4.0.2",
      "schematics>=1.0-0",
      "motor>=0.2"
    ]
)
import os
from setuptools import setup

setup(
    name = "smallscheme",
    version = "0.0.1",
    author = "John Jacobsen",
    author_email = "eigenhombre@gmail.com",
    description = ("A small implementation of enough Scheme "
                   "to follow along in SICP"),
    license = "MIT",
    keywords = "lisp sicp scheme",
    url = "https://github.com/eigenhombre/smallscheme",
    packages = ['smallscheme'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Languages",
        "License :: OSI Approved :: MIT License",
    ],
)

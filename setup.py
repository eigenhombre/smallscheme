import os
from setuptools import setup
import versioneer

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="smallscheme",
    author="John Jacobsen",
    author_email="eigenhombre@gmail.com",
    description=("A small implementation of enough Scheme "
                 "to follow along in SICP"),
    license="MIT",
    keywords="lisp sicp scheme",
    url="https://github.com/eigenhombre/smallscheme",
    packages=['smallscheme'],
    entry_points={
        'console_scripts': [
            'smallscheme = smallscheme.scheme:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)

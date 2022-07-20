import os
from setuptools import setup
import versioneer


desc = ("A small implementation of enough Scheme "
        "to follow along in SICP")
homeurl = "https://github.com/eigenhombre/smallscheme"


setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="smallscheme",
    author="John Jacobsen",
    author_email="eigenhombre@gmail.com",
    description=desc,
    long_description=(desc +
                      ".  See " + homeurl +
                      " for more information."),
    license="MIT",
    keywords="lisp sicp scheme",
    url=homeurl,
    packages=['smallscheme'],
    entry_points={
        'console_scripts': [
            'smallscheme = smallscheme.main:main',
        ],
    },
    install_requires=[
        'lark-parser == 0.7.3',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)

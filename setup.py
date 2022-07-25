import os
from setuptools import setup
import versioneer


desc = ("A small Scheme implementation, whose aim is to provide enough "
        "functionality to be used to run examples and work problems in SICP")
homeurl = "https://github.com/eigenhombre/smallscheme"


setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="smallscheme",
    author="John Jacobsen",
    author_email="eigenhombre@gmail.com",
    python_requires=">=3.5",
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
        'lark == 1.1.2',
        'prompt_toolkit == 3.0.30',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)

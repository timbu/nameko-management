#!/usr/bin/env python
from setuptools import setup

setup(
    name='nameko-management',
    version='0.0.1',
    description='Management framework for nameko services',
    author='timbu',
    url='http://github.com/timbu/nameko-management',
    py_modules=['nameko_management'],
    install_requires=[
        "nameko>=2.3.1",
    ],
    extras_require={
        'dev': [
            "coverage==4.1.0",
            "flake8==2.6.0",
            "pylint==1.5.5",
            "pytest==2.9.2",
        ]
    },
    dependency_links=[],
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)

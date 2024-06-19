#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = "1.0.0"

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="clisyncdemo",
    version=__version__,
    author="Edward Laurence",
    author_email="edwardl@hectiq.ai",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "clisyncdemo=clisyncdemo:main",
        ],
    },
)

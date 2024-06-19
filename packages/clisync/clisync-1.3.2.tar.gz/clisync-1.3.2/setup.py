#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = "1.3.2"

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="clisync",
    version=__version__,
    description="Generate click commands from your project",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Edward Laurence",
    author_email="edwardl@hectiq.ai",
    url="https://clisync.surge.sh",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="pip requirements imports",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
    ],
)

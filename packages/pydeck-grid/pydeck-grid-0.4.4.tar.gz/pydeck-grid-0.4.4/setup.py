#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import pydeck_grid
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["pydeck", "xarray", "orjson", "matplotlib"]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author="Oceanum Developers",
    author_email="developers@oceanum.science",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Pydeck layers for gridded data",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=False,
    keywords="pydeck gridded xarray",
    name="pydeck-grid",
    packages=find_packages(exclude=["tests", "docs"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/oceanum-io/pydeck_grid",
    version=pydeck_grid.__version__,
    zip_safe=False,
)

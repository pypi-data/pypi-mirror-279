#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="astro-eddy",
    version="2.4.1",
    author="Richard Teague",
    author_email="rteague@mit.edu",
    description=("Tools to study the dynamics of protoplanetary disks."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richteague/eddy",
    packages=["eddy"],
    license="MIT",
    install_requires=[
        "scipy>=1",
        "numpy",
        "matplotlib>=3",
        "emcee>=3",
        "corner>=2",
        "zeus-mcmc",
        "bettermoments",
        ],
    package_data={'eddy': ['*.yml']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

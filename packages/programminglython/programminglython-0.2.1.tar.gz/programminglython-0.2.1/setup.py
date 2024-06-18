#!/usr/bin/env python
import Lython
from os import path


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name='programminglython',
    version=Lython.__version__,
    description="Lython programming language built on top of CPython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=Lython.__author__,
    author_email=Lython.__email__,
    url=Lython.__url__,
    packages=["Lython"],
    scripts=["bin/lython"],
    license=Lython.__license__,
    platforms="any",
    install_requires=["var_dump"]
)

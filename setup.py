#!/usr/bin/env python
from distutils.core import setup

setup(
    name="tormor",
    version="1.0.0",
    description="Database migration helper",
    author="Tle Ekkul",
    author_email="aryuth.ekkul@proteus-tech.com",
    url="https://github.com/proteus-tech/tormor",
    scripts=["bin/tormor"],
    packages=["tormor"],
    install_requires=["psycopg2-binary"],
    data_files=[],
)

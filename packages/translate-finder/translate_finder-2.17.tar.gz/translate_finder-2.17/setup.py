#!/usr/bin/env python

# Copyright ©khulnasoft-bot <info@khulnasoft.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Setup file for easy installation."""

from setuptools import setup

with open("requirements.txt") as handle:
    REQUIRES = handle.read().splitlines()

setup(
    install_requires=REQUIRES,
)

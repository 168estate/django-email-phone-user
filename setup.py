#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from email_phone_user import version


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""

setup(
    name="django-email-phone-user",
    version=version,
    packages=find_packages(),
    test_suite="nose.collector",
    tests_require=["nose", "mock"],

    # metadata for upload to PyPI
    author="168 Estate Limited",
    author_email="info@168.estate",
    url="https://github.com/168estate/django-email-phone-user",
    description="Django Custom User model with email or phone as username",
    long_description=read('README.rst'),

    # Full list:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)

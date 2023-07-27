# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="pytbai",
    version="1.4.0",
    description=(
        "pytbai allows to create, manage and send TicketBai invoices to the"
        " Basque tax authorities"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Urtzi Odriozola",
    author_email="uodriozola@codesyntax.com",
    url="https://github.com/codesyntax/pytbai",
    license=license,
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="pytbai",
    version="0.1.0",
    description=(
        "pytbai allows to create, manage and send TicketBai invoices to the"
        " Basque tax authorities"
    ),
    long_description=readme,
    author="Urtzi Odriozola",
    author_email="uodriozola@codesyntax.com",
    url="https://github.com/codesyntax/pytbai",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)

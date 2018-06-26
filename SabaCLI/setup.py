#!/usr/bin/python3
# coding: utf-8
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


def main():
    setup(
        name="pySabaCLI",
        version="1.0.0",
        description="RyuGoo-Saba: a CWL-based execution engine utilizing cloud resources for big data analysis in life science",
        author="Hirotaka Suetake",
        author_email="hirotaka.suetake@rhelixa.com",
        url="https://github.com/Rhelixa-inc/RyuGoo-Saba",
        license="GPLv3",
        packages=["pySabaCLI"],
        entry_points={"console_scripts": ["saba = pySabaCLI.__main__:main"]},
        zip_safe=False,
        include_package_data=True,
        install_requires=requirements
    )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def get_version():
    """Get version from the package without actually importing it."""
    init = read("jarpcdantic_clients/__init__.py")
    for line in init.split("\n"):
        if line.startswith("__version__"):
            return eval(line.split("=")[1])


def get_requirements(select: list[str] | None = None) -> list[str]:
    """Get requirements from the package without actually importing it."""
    requirements = read("requirements.txt").split("\n")
    if select:
        requirements = [r for r in requirements if any(s in r for s in select)]
    return requirements


setup(
    name="jarpcdantic_clients",
    version=get_version(),
    packages=["jarpcdantic_clients"],
    description="Transports for JARPCdantic",
    extras_require={
        "cabbagok": get_requirements(["cabbagok"]),
        "aiohttp": get_requirements(["aiohttp"]),
        "requests": get_requirements(["requests"]),
        "all": get_requirements(),
    },
    python_requires=">=3.12",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    maintainer="WhiteApfel",
    maintainer_email="white@pfel.ru",
    url='https://github.com/whiteapfel/jarpcdantic_clients/',
    download_url='https://pypi.org/project/jarpcdantic_clients/',
    license="Mozilla Public License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Utilities",
    ],
)

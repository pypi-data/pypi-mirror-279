import os
import codecs
import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="ploomy",
    version=get_version("ploomy/__init__.py"),
    packages=[package for package in find_packages()],
    install_required=["pydantic"],
    long_description=README,
    long_description_content_type="text/markdown",
    description="A Python SDK for bloomd server.",
    author="Siddhartha Dhar Choudhury",
    author_email="sdharchou@gmail.com",
    url="https://github.com/frankhart2018/bloomy",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

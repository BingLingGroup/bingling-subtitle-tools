#!/usr/bin/env python
from setuptools import setup

# Get the version.py from bingling-subtitle-tools/version.py without importing the package
version = {}
with open("bingling-subtitle-tools/version.py") as fp:
    exec(fp.read(), version)
__version__ = version["__version__"]

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name="bingling_subtitle_tools",
    version=__version__,
    description="A tool that do batch processing jobs on ASS(Advanced SubStation Alpha)/SSA(Sub Station Alpha) files",
    author="BingLingGroup",
    author_email="binglingfansub@gmail.com",
    url="https://github.com/BingLingGroup/bingling-subtitle-tools",
    py_modules=["batch"],
    packages=["bingLing_subtitle_tools"],
    data_files=[("", ["README.rst"])],
    install_requires=["setuptools", "chardet"],
    entry_points="""
    [console_scripts]
    BingLing_Subtitle_Tools = batch:main
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
    long_description=long_description
)
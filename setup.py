#!/usr/bin/env python
import setuptools
import os

# Get the version from bingling-subtitle-tools/version.py without importing the package
version = {}
with open("bingling_subtitle_tools/version.py") as fp:
    exec(fp.read(), version)
__version__ = version["__version__"]

with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name="bingling_subtitle_tools",
    version=__version__,
    description="A tool that do batch processing jobs on ASS(Advanced SubStation Alpha) files",
    long_description=long_description,
    author="BingLingFanSub",
    author_email="binglingfansub@gmail.com",
    url="https://github.com/BingLingGroup/bingling-subtitle-tools",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "chardet"
    ],
    data_files=[("", ["README.md"])],
    entry_points="""
    [console_scripts]
    bingling_subtitle_tools = bingling_subtitle_tools.bingling_subtitle_tools.__init__:main
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ]
)

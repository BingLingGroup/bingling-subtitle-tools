#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://github.com/kennethreitz/setup.py/blob/master/setup.py
# Note: To use the "upload" functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "bingling_subtitle_tools"
DESCRIPTION = "A tool that do batch processing jobs on ASS(Advanced SubStation Alpha) files."
URL = "https://github.com/BingLingGroup/bingling-subtitle-tools"
EMAIL = "binglingfansub@gmail.com"
AUTHOR = "BingLingFanSub"
REQUIRES_PYTHON = ">=3.4.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "chardet"
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn"t have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "version.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup_0.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup_0.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    # If your package is a single module, use this instead of "packages":
    # py_modules=["mypackage"],

    entry_points="""
        [console_scripts]
        bingling-subtitle-tools = bingling_subtitle_tools:main
        """,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
    # $ setup_0.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
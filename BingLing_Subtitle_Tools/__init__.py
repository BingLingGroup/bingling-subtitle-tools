#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""initial module
"""


# Import built-in modules
import argparse
import codecs
import os
import re
import sys


# Import third-party modules
import chardet
import click


# Any changes to the path and your own modules
import ass_v4plus_process


def main():
    print()
    import_dir = "E:\\用户\\Documents\\CL字幕\\2018\\试制"
    export_dir = import_dir + "\\new"
    name_tail = "_new"
    sect = ("[Aegisub Project Garbage]", "[test]")
    version = {}
    with open("version.py") as fp:
        exec(fp.read(), version)
    __version__ = version["__version__"]

    special_msg = "# Exported by BingLing-Subtitle-Tools {ver}".format(ver=__version__)

    ass_v4plus_process.simple_ass_export_batch(import_dir, export_dir, special_msg)

    # ass_v4plus_process.delete_ass_sect_batch(import_dir, export_dir, sect=sect)


if __name__ == "__main__":
    main()













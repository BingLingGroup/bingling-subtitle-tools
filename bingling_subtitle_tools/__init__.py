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
    import_dir = "E:\\用户\\Documents\\CL字幕\\2018\\2015字幕成品\\时间轴\\S1"
    export_dir = import_dir + "\\new"
    name_tail = "_new"
    sect = ("[Aegisub Project Garbage]", "[test]")
    version = {}
    with open("version.py") as fp:
        exec(fp.read(), version)
    __version__ = version["__version__"]

    special_msg = "# Exported by BingLingSubtitleTools {ver}".format(ver=__version__)

    if os.path.exists(export_dir) is False:
        os.makedirs(export_dir)
    ass_v4plus_process.simple_ass_export_batch(import_dir, export_dir, special_msg, export_method=(True, False))

    # ass_v4plus_process.delete_ass_sect_batch(import_dir, export_dir, sect=sect)


if __name__ == "__main__":
    main()













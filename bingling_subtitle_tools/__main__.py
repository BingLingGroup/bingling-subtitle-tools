#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""description
"""

# Import built-in modules
import sys

# Import third-party modules


if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    # Reference: https://github.com/rg3/youtube-dl/blob/master/youtube_dl/__main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

# Any changes to the path and your own modules
import bingling_subtitle_tools

if __name__ == "__main__":
    bingling_subtitle_tools.main()

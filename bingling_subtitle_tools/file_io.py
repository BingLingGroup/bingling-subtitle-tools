#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""file_io module
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


def get_files_name_from_dire(dire, exte=(".ass", ".ssa")):
    """Get files name from the given directory.

    Params:
    dire                -- a directory String
    exte                -- extensions Tuple

    Return:
    files_name_list     -- a file name list contains files whose extension
                        -- matches the given string exte
    """

    files_name_list = []
    for file_name in os.listdir(dire):
        if file_name.startswith("."):
            continue
        for exte_e in exte:
            if file_name.endswith(exte_e):
                files_name_list.append(file_name)
    return files_name_list


def file_to_list(file_name, file_line_list, is_forced_lf=True):
    """Read a file to a list.

    Params:
    file_name           -- a file with file_name about to be read
    file_line_list      -- a result list, a line per elem
    is_forced_lf        -- force utf-8 without BOM and unix LF file input
                           True by default

    Return:
    fail_c              -- the count for file opening failure
    in_codec            -- the file input codec
    is_crlf             -- True for a windows .ass file, False for a unix .ass file

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT LICENSE
    """

    fail_c = 0
    in_codec = codecs.lookup("utf-8")
    crlf_is_detected = False
    is_crlf = True

    try:
        with open(file_name, "rb") as in_file:
            in_codec = codecs.lookup(detect_charset(in_file))
            file_decoded = in_codec.streamreader(in_file)
            for line in file_decoded:
                if line != "\r\n" and line != "\n":
                    # not windows CRLF or unix LF
                    line = line.strip()
                elif is_forced_lf is False and crlf_is_detected is False:
                    crlf_is_detected = True
                    if line == "\r\n":
                        is_crlf = True
                    else:
                        is_crlf = False
                elif is_forced_lf is True:
                    is_crlf = True
                    if line == "\r\n":
                        line = "\n"

                file_line_list.append(line)

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c += 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c += 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c += 1

    return fail_c, in_codec, is_crlf


def list_to_file(out_codec, file_name, file_line_list, is_lf=True):
    """Write a list to a file.

    Params:
    out_codec           -- the output file codec,
                           functioned when is_lf is True
    file_name           -- a file with file_name about to be read
    file_line_list      -- a result list, a line per elem
    is_lf               -- True for unix LF and UTF-8 without BOM file output
                           False for windows CRLF and dedicated codec or UTF-8 with BOM

    Return:
    fail_c              -- the count for file writing failure

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT LICENSE
    """

    fail_c = 0
    out_str = ""

    if is_lf:
        # unix LF
        for elem in file_line_list:
            out_str += elem
            if elem != "\n":
                out_str += "\n"
    else:
        # windows CRLF
        for elem in file_line_list:
            out_str += elem
            if elem != "\r\n":
                out_str += "\r\n"

    try:
        if is_lf:
            # write unix LF and UTF-8 without BOM
            with open(file_name, "w", encoding="utf-8") as out_file:
                out_file.write(out_str)

        else:
            # write windows CRLF and dedicated codec or UTF-8 with BOM
            with open(file_name, "wb") as out_file:
                out_file.write(out_codec.encode(out_str)[0])

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c += 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c += 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c += 1

    return fail_c


def file_to_str(file_name):
    """Read a file to a multi-line string.

    Params:
    file_name       -- a file with file_name about to be read

    Return:
    fail_c          -- the count for file opening failure
    in_codec        -- the file input codec
    file_str        -- a result multi-line string

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT LICENSE
    """

    fail_c = 0
    in_codec = codecs.lookup("utf-8")
    file_str = ""

    try:
        with open(file_name, "rb") as in_file:
            in_codec = codecs.lookup(detect_charset(in_file))
            file_str = in_codec.streamreader(in_file)

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c += 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c += 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c += 1

    return fail_c, in_codec, file_str


def str_to_file(out_codec, out_name, out_str, is_lf=True):
    """Write a string to a file.

    Params:
    out_codec       -- the output file codec
    out_name        -- a file with out_name about to be read
    out_str         -- a result list, a line per elem
    is_lf           -- True for unix LF and UTF-8 without BOM file output
                       False for windows CRLF and dedicated codec or UTF-8 with BOM

    Return:
    fail_c          -- the count for file writing failure

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT LICENSE
    """

    fail_c = 0

    try:
        if is_lf:
            # write unix LF and UTF-8 without BOM
            with open(out_name, "w", encoding="utf-8") as out_file:
                out_file.write(out_str)

        else:
            # write windows CRLF and dedicated codec or UTF-8 with BOM
            with open(out_name, "wb") as out_file:
                out_file.write(out_codec.encode(out_str)[0])

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c += 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c += 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c += 1

    return fail_c


def detect_charset(file):
    """Detect the charset of file, using chardet module,
    return the name of charset or exit.

    Params:
    file_name                   -- a file with file_name about to be read
    file_line_list              -- a result list, a line per elem

    Return:
    chardet_result["encoding"]  -- the name of the charset

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT LICENSE
    """

    sample = file.read(4096)
    file.seek(0)
    chardet_result = chardet.detect(sample)
    if chardet_result["confidence"] < 0.3:
        print("Error: unknown file encoding", file=sys.stderr)
        sys.exit(1)
    elif chardet_result["confidence"] < 0.6:
        print("Warning: uncertain file encoding", file=sys.stderr)
    if chardet_result["encoding"] == "GB2312":
        return "GB18030"
    return chardet_result["encoding"]


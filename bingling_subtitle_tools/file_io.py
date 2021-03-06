#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""file_io module
"""


# Import built-in modules
import codecs
import os
import sys


# Import third-party modules
import chardet


# Any changes to the path and your own modules


def get_files_name_from_dire(dire, exte=(".ass", ".ssa")):
    """Get files name from the given directory.

    Params:
    dire                -- a directory String
    exte                -- extensions filter tuple

    Return:
    files_name_list     -- a file name list contains files whose extension
                        -- filters the given string exte
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
    is_lf               -- True for a unix .ass file, False for a windows .ass file

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT_LICENSE
    """

    fail_c = 0
    in_codec = codecs.lookup("utf-8")
    is_lf = False

    try:
        with open(file_name, "rb") as in_file:
            in_codec = codecs.lookup(detect_charset(in_file))
            file_decoded = in_codec.streamreader(in_file).read()
            if "\r\n" in file_decoded:
                if is_forced_lf is False:
                    file_line_list.extend(file_decoded.split("\r\n"))
                    is_lf = False
                else:
                    file_line_list.extend(file_decoded.split("\r\n"))
                    is_lf = True
            else:
                file_line_list.extend(file_decoded.split("\n"))
                is_lf = True

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c = 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c = 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c = 1

    return fail_c, in_codec, is_lf


def list_to_file(out_codec, out_name, file_line_list, is_lf=True):
    """Write a list to a file.

    Params:
    out_codec           -- the output file codec,
                           functioned when is_lf is True
    out_name            -- a file with out_name about to be read
    file_line_list      -- a result list, a line per elem
    is_lf               -- True for unix LF and UTF-8 without BOM file output
                           False for windows CRLF and dedicated codec or UTF-8 with BOM

    Return:
    fail_c              -- the count for file writing failure

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT_LICENSE
    """

    fail_c = 0
    out_str = ""

    if is_lf:
        # unix LF
        out_str = "\n".join(file_line_list)
    else:
        # windows CRLF
        out_str = "\r\n".join(file_line_list)

    try:
        if is_lf:
            # write unix LF and UTF-8 without BOM
            out_codec = codecs.lookup("utf-8")

        # write windows CRLF and dedicated codec or UTF-8 with BOM
        with open(out_name, "wb") as out_file:
            out_file.write(out_codec.encode(out_str)[0])

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c = 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c = 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c = 1

    return fail_c


def file_to_str(file_name):
    """Read a file to a multi-line string.

    Params:
    file_name       -- a file with file_name about to be read

    Return:
    fail_c          -- the count for file opening failure
    in_codec        -- the file input codec
    file_str        -- a result multi-line string

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT_LICENSE
    """

    fail_c = 0
    in_codec = codecs.lookup("utf-8")
    file_str = None

    try:
        with open(file_name, "rb") as in_file:
            in_codec = codecs.lookup(detect_charset(in_file))
            file_str = in_codec.streamreader(in_file).read()

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c = 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c = 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c = 1

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

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT_LICENSE
    """

    fail_c = 0

    try:
        if is_lf:
            # write unix LF and UTF-8 without BOM
            out_codec = codecs.lookup("utf-8")

        # write windows CRLF and dedicated codec or UTF-8 with BOM
        with open(out_name, "wb") as out_file:
            out_file.write(out_codec.encode(out_str)[0])

    except (UnicodeDecodeError, UnicodeEncodeError, LookupError) as e:
        print("[fail] (codec error)")
        print(e, file=sys.stderr)
        fail_c = 1
    except ValueError as e:
        print("[fail] (irregular format)")
        print(e, file=sys.stderr)
        fail_c = 1
    except IOError as e:
        print("[fail] (IO error)")
        print(e, file=sys.stderr)
        fail_c = 1

    return fail_c


def detect_charset(file):
    """Detect the charset of file, using chardet module,
    return the name of charset or exit.

    Params:
    file_name                   -- a file with file_name about to be read
    file_line_list              -- a result list, a line per elem

    Return:
    chardet_result["encoding"]  -- the name of the charset

    Modified from https://github.com/sorz/asstosrt. See /asstosrt/MIT_LICENSE
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


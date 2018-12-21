#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An example bingling-subtitle-tools .py config file
"""

# bingling-subtitle-tools can do batch processing jobs on ASS
# (Advanced SubStation Alpha) files
# Reference: http://moodub.free.fr/video/ass-specs.doc
#            https://github.com/sorz/asstosrt
# Author: BingLingFanSub
# Bug report: https://github.com/BingLingGroup/bingling-subtitle-tools

# Comment usage
# Prepend a # to the line you want to comment.

# Escape sequence usage
# Backslash is an escape sequence to specify the actual String.
# Use an escape sequence for using a double quote itself
# in a double quoted String and vice versa.
# String can be prefixed with a letter "r" or "R"
# to avoid using such an escape sequence.
# Such a string is called raw strings and treat backslashes as literal characters.
# Escape sequence like "\n" won't work as well.

# String usage
# Make sure the strings have delimiters.
# Single quote('') or double quotes("") as String's delimiters are both fine.

# Multi-line String usage
# https://docs.python.org/3/tutorial/introduction.html#strings

# Tuple usage (when its item is String)
# ["xxx"], ["xxx", "xxx"]

# Path example
# Bad example will fail.
# good e.g. with forward slashes
# windows absolute path
# "X:\\xxx\\xxx\\" or "X:\\xxx\\xxx"
# "X:/xxx/xxx/" or "X:/xxx/xxx"
# r"X:\xxx\xxx\" or r"X:\xxx\xxx\"
# windows relative path or unix path
# "/xxx/xxx" or "\xxx\xxx"
# bad e.g. with single backslash
# or without quotes as delimiters
# X:\xxx\xxx (Like the paths in windows file explorer)

# Make sure the arguments are put on the right side of the equal sign.
# The "default" in the comment means
# if this config file don't contain this option,
# the program will set a default value for it.
# The "arg_num" in the comment means if the option is input, the number of arguments is required.
# The "arg_type" in the comment means the argument type. Make sure the arguments are used in the proper way.
# The "-xx: " in the help means it works when "xx" option is input.
# If you are not using the function, you can omit it and its sub options

input_ = ["D:\\example\\input", ]
# Path(s) or file name(s) of the input .ass file(s).
# arg_type = Tuple
# default = (current command line direction)
# arg_num ≥ 0

output = ["D:\\example\\output", ]
# Name(s) of the output directory.
# Functions when direction(s) exist(s)
# and it has the same number of the input.
# Otherwise it will try to make a new folder named \"new\"
# in the input directory
# arg_type = Tuple
# default = (Make a new folder named \"new\" in the input directory)
# arg_num ≥ 0

exp_smp = True
# Enable a function:
# do a batch job on exporting .ass file(s) to txt file(s).
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

field_name = "Style"
# -es: A Field name to separate .ass files into txt files.
# Functions when -es is used.
# arg_type = String (Recommend using the event field name in .ass)
# default = Style
# arg_num = 0 or 1

custom_msg = " "
# -es: A custom message is written
# on the first line of the output files.
# "" (nothing) for no extra message export
# arg_type = String
# default = "# Exported by BingLingSubtitleTools x.x.x"
# (x.x.x means current package version)
# arg_num = 0 or 1

name_tails = ["_CN", "_EN", ]
# -es: The output files' name tail(s).
# [] (only two square brackets) for no specific name tails
# which means using each event's specific field content
# as their name tail.
# Functions when name tails have the same number as
# the ones after \"filter\".
# arg_type = Tuple
# default = ["_CN", "_EN", ]
# arg_num ≥ 0

filter_ = ["中文字幕", "英文字幕", ]
# -es: Field content(s) to filter the events.
# [] for filter disabled and all the events will export to files
# separated by their field contents under the specific field name.
# arg_type = Tuple
# default = ["中文字幕", "英文字幕", ]
# arg_num ≥ 0

text_excluded = False
# -es: Enable output for text-excluded part,
# which is separated into a file with a "_t" name tail
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

rename_number = False
# -es: Enable changing the export name into
# a kind of format like "E" + the number already in the file name.
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

keep_override_code = False
# Keep the override codes (similar words are override tags
# by http://docs.aegisub.org/3.2/ASS_Tags/) instead of deleting them.
# default = False
# [arg_num = 0]

no_forced_encoding = False
# Disable output file encoding into utf-8 without BOM
# equal to utf-8 with unix LF and it will use the same encoding
# as the input file with the windows CRLF.
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

limited_output = False
# Limit the files to one path
# which is the first \"-o/--output\" argument.
# At least one output path must be specified.
# Or it will be overridden.
# default = False
# [arg_num = 0]

del_sect = False
# Enable a function: do a batch job on deleting .ass section(s) in .ass file(s).
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

sect_name = ["[Aegisub Project Garbage]", ]
# ds: The section name(s) to Delete.
# arg_type = Tuple
# default = ["[Aegisub Project Garbage]", ]
# arg_num > 0

name_tail = "_new"
# -ds: The output files' name tail.
# [] for no name tail output.
# arg_type = String
# default = "_new"
# arg_num = 0 or 1

overwrite = False
# -ds: [WARNING] Enable overwriting files.
# Using this option will override the "-o/--output" option
# and the "-nt/--name-tail" option.
# Not using this option will prevent any attempts to overwrite the files.
# arg_type = Boolean (True/False) (Remember to capitalize)
# default = False
# arg_num = 0

# the code below is a config without comments
# input_ = [r"D:\example\input", ]
# output = [r"D:\example\output", ]
# exp_smp = True
# field_name = "Style"
# custom_msg = " "
# name_tails = ["_CN", "_EN", ]
# filter_ = ["中文字幕", "英文字幕", ]
# text_excluded = False
# rename_number = False
# keep_override_code = False
# no_forced_encoding = False
# limited_output = True
# del_sect = False
# sect_name = ["[Aegisub Project Garbage]", ]
# name_tail = "_new"
# overwrite = False

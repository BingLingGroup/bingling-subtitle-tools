#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An example .py config file
"""

# Slash usage.
# good e.g. with forward slashes
# windows absolute path
# "X:\\xxx\\xxx\\" or "X:\\xxx\\xxx"
# "X:/xxx/xxx/" or "X:/xxx/xx"
# windows relative path or unix path
# "/xxx/xxx" or "\xxx\xxx"
# bad e.g. with backslashes or without quotes
# X:\xxx\xxx (Like the paths in windows file explorer)

# Make sure the strings are in quotes.
# The default value is used when the option is not present at the command line.
# The "arg_num" in the help means if the option is input, the number of arguments is required.
# The "-xx: " in the help means it works when "xx" option is input.

input_ = "D:\\example\\input"
# Path(s) or file name(s) of the input .ass file(s).
# [arg_num ≥ 0]
# [default: Command line current directory]

output = "D:\\example\\output"
# Name(s) of the output directory.
# Functions when direction(s) exist(s)
# and it has the same number of the input.
# [arg_num ≥ 0]
# [default: Make a new folder named \"new\"
# in the input directory]

exp_smp = True
# "Enable a function:
# do a batch job on exporting .ass file(s) to txt file(s).
# [arg_num = 0]

field_name = "Style"
# A Field name to separate .ass files into txt files.
# Using the option without argument for default value.
# Functions when -es is used.
# [arg_num = 0 or 1]
# [default: Style]

custom_msg = " "
# A custom message is written
# on the first line of the output files.
# Using the option without argument for no extra message output.


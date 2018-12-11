#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""initial module
"""


# Import built-in modules
import os


# Import third-party modules
import click


# Any changes to the path and your own modules
import ass_v4p_prcs


def _get_args():
    pass
    # parser = argparse.ArgumentParser(description=description,
    #                                  epilog="Author: " + author + " <" + author_email + ">" \
    #                                         + "bug report: " + url)
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument("-ds", "--del-sect", action="store_true")
    # group.add_argument("-es", "--exp-smp", action="store_true")
    #
    # parser.add_argument("-o", "--output-dir", default=os.getcwd() + "\\new")
    # parser.add_argument("-i", "--input-dir", default=os.getcwd())

    # return parser.parse_args()


def main():
    pass
    # print()
    # # import_dir = "E:\\用户\\Documents\\CL字幕\\2018\\试制\\test"
    # import_dir = "E:\\用户\\Documents\\CL字幕\\2018\\2015字幕成品\\时间轴\\S1"
    # export_dir = import_dir + "\\new"
    # name_tail = "_new"
    # sect = ("[Aegisub Project Garbage]", "[test]")
    #
    # # special_msg = "# Exported by BingLingSubtitleTools {ver}".format(ver=__version__)
    #
    # if os.path.exists(export_dir) is False:
    #     os.makedirs(export_dir)
    # # ass_v4p_prcs.simple_ass_export_batch(import_dir, export_dir, special_msg,
    # #                                      export_method=(True, True), content_tuple=None)
    #
    # # ass_v4plus_process.delete_ass_sect_batch(import_dir, export_dir, sect=sect)


@click.command()
@click.option("-i", "--input", "input_",
              default=os.getcwd(), nargs=1,
              type=click.Path(dir_okay=True, file_okay=True),
              help="Paths or file names of the input .ass files. \
[default: Current directory]", multiple=True)
@click.option("-o", "--output", default=os.getcwd() + "\\new",
              nargs=1,
              type=click.Path(dir_okay=True, file_okay=True),
              help="Name of the output directory. \
[default: Make a new folder named \"new\" \
in the current directory]")
@click.option("-es", "--export-simply", default=False,
              show_default=True, is_flag=True,
              help="Do a batch job on exporting .ass files to txt files.")
@click.option("-fn", "--field_name", nargs=1, default="Style",
              metavar="FIELD_NAME", show_default=True,
              help="-es: A Field name to separate .ass files into txt files. \
This will function when -es is used. \
Help below will use \"-xx: \" to indicate \
a sub option function after which main option")
@click.option("-msg", "--custom-msg", nargs=1, type=click.STRING,
              default="# Exported by BingLingSubtitleTools x.x.x",
              metavar="STRING", show_default=True,
              help="-es: A special message in quotes is written \
on the first line of the output files. \
Input \"None\" for no extra message output.")
@click.option("-nts", "--name-tails", nargs=1, type=click.STRING,
              default="_CN, _EN", metavar="STRING",
              show_default=True, multiple=True,
              help="-es: The output files' name tail(s).\
Support multiple arguments input. \
This will function when name tails have the same number as \
the ones after \"match\". \
The default \"..., ...\"means if there's no using of this option, \
it will try these 2 arguments: _CN, _EN \
Same info omit below.")
@click.option("-mt", "--match", nargs=1, type=click.STRING,
              default="中文字幕, 英文字幕", show_default=True, multiple=True,
              metavar="STRING",
              help="-es: Several field contents under the same field name \
to separate .ass files to txt files. \
Support multiple arguments input.")
@click.option("-te", "--text-excluded", default=False,
              show_default=True, is_flag=True,
              help="-es: Enable output for text-excluded parts, \
which are separated into the files with a \"_t\" name tail")
@click.option("-rn", "--rename-number", default=False,
              show_default=True, is_flag=True,
              help="-es: Enable changing the export name into \
a kind of format like \"E\" + the number already in the file name.")
@click.option("-nfe", "--no-forced-encoding", default=False,
              show_default=True, is_flag=True,
              help="-es: Disable output file \
encoding into utf-8 without BOM, equal to utf-8 with unix LF.\
Instead it will use the same encoding as the input file and the windows CRLF.")
@click.option("-ds", "--delete-section", default=False,
              show_default=True, is_flag=True,
              help="Delete .ass sections in .ass files.")
@click.option("-sc", "--sect_name", nargs=1,
              default="[Aegisub Project Garbage]", metavar="STRING",
              show_default=True, multiple=True,
              help="-ds: The section name(s) to Delete. \
This will function when -es is used. \
Help below will use \"-xx: \" to indicate \
a sub option function after which main option")
@click.option("-nt", "--name-tail", nargs=1, type=click.STRING,
              default="_new", metavar="STRING",
              show_default=True,
              help="-ds: The output files' name tail.")
@click.help_option("-h", "--help")
def cli0(input_,
         output,
         export_simply,
         field_name,
         custom_msg,
         name_tails,
         match,
         text_excluded,
         rename_number,
         no_forced_encoding,
         delete_section,
         sect_name,
         name_tail):
    """A tool that do a batch processing job on ASS(Advanced SubStation Alpha) files

     Multiple arguments input e.g. -option argument_1 -option argument_2

     Reference: http://moodub.free.fr/video/ass-specs.doc

     Author: BingLingFanSub

     Bug report: https://github.com/BingLingGroup/bingling-subtitle-tools
    """
    version = {}
    with open("version.py") as fp:
        exec(fp.read(), version)
    __version__ = version["version"]
    print(input_)
    print(output)
    print(export_simply)
    print(custom_msg)
    print("# Exported by BingLingSubtitleTools {cur_ver}".format(cur_ver=__version__))
    print(delete_section)


if __name__ == "__main__":
    cli0()















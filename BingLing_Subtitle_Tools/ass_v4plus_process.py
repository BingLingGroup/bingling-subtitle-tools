#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ass_v4plus_classes
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
import file_io


class GetFieldContentFailedException(Exception):
    """Failed to initialize a SimpleAssEvent class
    """

    def __init__(self):
        Exception.__init__(self)


class SimpleAssEvent:
    """Simple class for ass event section

        ref http://moodub.free.fr/video/ass-specs.doc
        """

    simple_event_fields = ["Marked", "Start", "End", "Style", "Name",
                           "MarginL", "MarginR", "MarginV",
                           "Effect"]
    field_content_list = []
    field_name = None

    def __init__(self,
                 event_line_list,
                 cur_row,
                 field_content_begin,
                 field_content_end,
                 first_text_begin,
                 field_name="Style",
                 ):
        """Initialize a SimpleAssEvent object from event_line_list

                    Params:
                    event_line_list         -- an .ass event section line list
                    cur_row                 -- current row num
                    field_content_begin     -- an .ass event field content begin pos in the first line
                    field_content_end       -- an .ass event field content end pos in the first line
                    first_text_begin        -- the text content begin pos in the first line
                    field_name              -- the condition of event classification
                    """

        _field_content_begin = field_content_begin
        _field_content_end = field_content_end
        _text_begin = first_text_begin
        self._field_content = \
            event_line_list[0][_field_content_begin:_field_content_end]
        self._text_list = [_text_begin, ]
        SimpleAssEvent.field_content_list.append(self._field_content)
        self._event_row = [cur_row, ]
        SimpleAssEvent.field_name = field_name

        for line in event_line_list[1:]:
            _field_content_begin, _field_content_end, _text_begin = \
                get_field_content_and_text(line, field_name)
            if line.startswith("Dialogue") and self._field_content == line[_field_content_begin:_field_content_end]:
                # if field content is the same and it starts with "Dialogue"
                # then append to the list
                self._text_list.append(_text_begin)
            else:
                self._event_row.append(cur_row + len(self._text_list))
                # a python slice end pos
                break

    def _add_more_events(self,
                         event_line_list,
                         cur_row,
                         first_text_begin,
                         ):
        """Initialize a SimpleAssEvent object from event_line_list

                    Params:
                    event_line_list         -- an .ass event section line list
                    cur_row                 -- current row num
                    first_text_begin        -- the text content begin pos in the first line
                    """

        _last_length = len(self._text_list)
        self._text_list.append(first_text_begin)
        self._event_row.append(cur_row)

        for line in event_line_list[1:]:
            _field_content_begin, _field_content_end, _text_begin = \
                get_field_content_and_text(line, SimpleAssEvent.field_name)
            if line.startswith("Dialogue") and self._field_content == line[_field_content_begin:_field_content_end]:
                # if field content is the same and it starts with "Dialogue"
                # then append to the list
                self._text_list.append(_text_begin)
            else:
                self._event_row.append(cur_row + len(self._text_list) - _last_length)
                break


class AssV4plusStyle:
    """Ass v4plus style section class

        ref http://moodub.free.fr/video/ass-specs.doc
        """

    def __init__(self,
                 name="default",
                 font_name="",
                 font_size=0.0,
                 primary_colour=0,
                 secondary_colour=0,
                 outline_colour=0,
                 back_colour=0,
                 bold=0,
                 italic=0,
                 under_line=0,
                 strike_out=0,
                 scale_x=0.0,
                 scale_y=0.0,
                 spacing=0.0,
                 angle=0.0,
                 border_style=0,
                 outline=0.0,
                 shadow=0.0,
                 alignment=0,
                 margin_l=0.0,
                 margin_r=0.0,
                 margin_v=0.0,
                 encoding=1
                 ):
        self._name = name
        # The name of the Style. Case sensitive. Cannot include commas.

        self._font_name = font_name
        # The font name as used by Windows. Case-sensitive.

        self._font_size = font_size
        # Value is float

        self._primary_colour = primary_colour
        # A long integer BGR (blue-green-red)  value. ie.
        # the byte order in the hexadecimal equivalent of this number is BBGGRR
        # This is the colour that a subtitle will normally appear in.

        self._secondary_colour = secondary_colour
        # A long integer BGR (blue-green-red) value. ie.
        # the byte order in the hexadecimal equivalent of this number is BBGGRR
        # This colour may be used instead of the Primary colour when a subtitle is automatically shifted
        # to prevent an onscreen collision, to distinguish the different subtitles.

        self._outline_colour = outline_colour
        #  A long integer BGR (blue-green-red)  value. ie.
        #  the byte order in the hexadecimal equivalent of this number is BBGGRR
        #  This colour may be used instead of the Primary or Secondary colour when a subtitle is automatically shifted
        #  to prevent an onscreen collision, to distinguish the different subtitles.

        self._back_colour = back_colour
        # This is the colour of the subtitle outline or shadow, if these are used.
        # A long integer BGR (blue-green-red)  value. ie.
        # the byte order in the hexadecimal equivalent of this number is BBGGRR.

        self._bold = bold
        # This defines whether text is bold (true) or not (false). -1 is True, 0 is False.

        self._italic = italic
        # This defines whether text is italic (true) or not (false). -1 is True, 0 is False.

        self._under_line = under_line
        # This defines whether text is underlined (true) or not (false). -1 is True, 0 is False.

        self._strike_out = strike_out
        # This defines whether text is strikeout (true) or not (false). -1 is True, 0 is False.

        self._scale_x = scale_x
        # Modifies the width of the font. Stays between 0.0 to 100.0 (percent)

        self._scale_y = scale_y
        # Modifies the height of the font. Stays between 0.0 to 100.0 (percent)

        self._spacing = spacing
        # Extra space between characters. Stands for pixels.

        self._angle = angle
        # The origin of the rotation is defined by the alignment. Can be a floating point number. Stands for degrees.

        self._border_style = border_style
        # 1 for outline and shadow style, 3 for opaque box style

        self._outline = outline
        # If BorderStyle is 1, then this specifies the width of the outline around the text, in pixels.

        self._shadow = shadow
        # If BorderStyle is 1, then this specifies the depth of the drop shadow behind the text, in pixels.
        # Thick outline with shadow is not recommended.
        # Shadow is not as effective as outline in terms of preventing an onscreen collision

        self._alignment = alignment
        # This sets how text is "justified" within the Left/Right onscreen margins, and also the vertical placing.
        # Values stays between 1 and 9.
        # eg. This is a screen: | 7 | 8 | 9 |
        #                       | 4 | 5 | 6 |
        #                       | 1 | 2 | 3 |
        # Numbers above are values of alignment.

        self._margin_l = margin_l
        # This defines the Left Margin in pixels.
        # It is the distance from the left-hand edge of the screen.
        # The three onscreen margins (MarginL, MarginR, MarginV) define areas
        # in which the subtitle text will be displayed.

        self._margin_r = margin_r
        # This defines the Right Margin in pixels.
        # It is the distance from the right-hand edge of the screen.
        # The three onscreen margins (MarginL, MarginR, MarginV) define areas
        # in which the subtitle text will be displayed.

        self._margin_v = margin_v
        # This defines the vertical Left Margin in pixels.
        # For a subtitle(alignment = 1/2/3), it is the distance from the bottom of the screen.
        # For a toptitle(alignment = 7/8/9), it is the distance from the top of the screen.
        # For a midtitle(alignment = 4/5/6), the value is ignored - the text will be vertically centred

        self._encoding = encoding
        # This specifies the font character set or encoding and on multi-lingual Windows installations.
        # It provides access to characters used in multiple than one languages.
        # It is usually 0 (zero) for English (Western, ANSI) Windows.
        # 1 for default encoding.
        # When the file is Unicode, this field is useful during file format conversions.


def get_field_content_and_text(line,
                               field_name="Style"):
    """Get field content and text from the given field name

        Params:
        field_name          -- the given field name, "Style" by default
                            -- but not "Text"

        Return:
        field_content_begin -- the field content beginning position
        field_content_end   -- the field content end position
        text_begin          -- the "Text" content beginning position
        """

    try:
        field_num = SimpleAssEvent.simple_event_fields.index(field_name)
    except ValueError:
        raise GetFieldContentFailedException

    field_content_begin = 0
    field_count = 0

    if field_num == 0:
        while field_content_begin < len(line):
            field_content_begin += 1
            if line[field_content_begin] == ":":
                field_content_begin += 2
                # jump ":" and " "
                break
    else:
        while field_content_begin < len(line) and field_count < field_num:
            if line[field_content_begin] == ",":
                field_count += 1
            field_content_begin += 1
            # field_content_begin will stop at the field's first char

    if field_content_begin == len(line):
        raise GetFieldContentFailedException

    if field_num >= len(SimpleAssEvent.simple_event_fields):
        return field_content_begin, len(line), 0

    field_content_end = field_content_begin

    while field_count < field_num + 1:
        if line[field_content_begin] == ",":
            field_count += 1
            break
        field_content_end += 1
        # field_content_end will stop at the next ","

    text_begin = field_content_end

    while field_content_begin < len(line) and field_count < len(SimpleAssEvent.simple_event_fields):
        if line[field_content_begin] == ",":
            field_count += 1
        text_begin += 1
        # text_begin will stop at the text's first char

    if text_begin == len(line):
        raise GetFieldContentFailedException

    return field_content_begin, field_content_end, text_begin


def simple_ass_export_txt(ass_file_line_list,
                          export_file_name,
                          special_msg,
                          name_tail=("_CN", "_EN"),
                          is_not_text=False,
                          field_name="Style",
                          content_tuple=("中文字幕", "英文字幕"),
                          is_forced_lf=True
                          ):
    """Get field content from the given field name

        Params:
        ass_file_line_list  -- an .ass file line list
        export_file_name    -- export file name
        special_msg         -- a special message write on the first line of the files
                               None for nothing to write
        name_tail           -- new files name tail tuple, ("_CN", "_EN") by default
                               if name_tail is not empty and it has the same length as the content_tuple
                               new files name will add one of these tails in order
                               otherwise the tail will be the field content
        export_method       -- a tuple includes two Boolean Objects
                               1st True for text-excluded content export method activated
                               otherwise it will only export text content
                               one .txt per one .ass field content
                               2nd True for changing export name into "E" + "%nd"
                               otherwise export name will stay the same
                               or add name_tail if content_tuple is not empty
        field_name          -- a field name to classify
                               ref http://moodub.free.fr/video/ass-specs.doc
        content_tuple       -- a content tuple to match, if it is None
                               it will export text grouped by field content
        is_forced_lf        -- force utf-8 without BOM and unix LF file input
                               True by default

        Return:
        matched_list        -- a list for the ones in content_tuple
                               match the field contents
                               [-1, ] for event section miss
                               [-2, ] for field content not match the content_tuple
        fail_c              -- the count for file failure
        """

    matched_list = []
    fail_c = 0

    simple_ass_event = None

    try:
        row_num = ass_file_line_list.index("[Events]")
    except ValueError:
        # can't find event section: return -1
        matched_list.append(-1)
        return matched_list, fail_c

    row_num += 1

    while row_num < len(ass_file_line_list):
        if ass_file_line_list[row_num].startswith("Dialogue"):
            try:
                field_content_begin, field_content_end, text_begin = \
                    get_field_content_and_text(ass_file_line_list[row_num])
            except GetFieldContentFailedException:
                # if it can't find the field content, then try the next line
                row_num += 1
                continue

            if content_tuple is not None:
                # first match the content_tuple
                try:
                    content_tuple.index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is not what we want, then try the next line
                    row_num += 1
                    continue

            # if the content_tuple doesn't exist
            # or we want to add the field content
            # we will create a new SimpleAssEvent object
            simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                              field_content_end, text_begin, field_name)
            row_num = simple_ass_event._event_row[-1]
            break

        else:
            # find first elem in simple_ass_event_list
            row_num += 1

    if simple_ass_event is not None:
        simple_ass_event_list = [simple_ass_event, ]
    else:
        # can't find any event that matched the field content
        matched_list.append(-2)
        return matched_list, fail_c

    while row_num < len(ass_file_line_list):
        if ass_file_line_list[row_num].startswith("Dialogue"):
            try:
                field_content_begin, field_content_end, text_begin = \
                    get_field_content_and_text(ass_file_line_list[row_num])
            except GetFieldContentFailedException:
                # if it can't find the field content, then try the next line
                row_num += 1
                continue

            if content_tuple is not None:
                # first match the content_tuple
                try:
                    i = content_tuple.index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is not what we want, then try the next line
                    row_num += 1
                    continue

                try:
                    j = SimpleAssEvent.field_content_list.index(content_tuple[i])
                except ValueError:
                    # if this field content is new to the field_content_list
                    # then create a new SimpleAssEvent object
                    simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                      field_content_end, text_begin, field_name)
                    row_num += len(simple_ass_event._text_list)
                    simple_ass_event_list.append(simple_ass_event)
                    continue

                # if this field content is already in the field_content_list
                # then add it
                simple_ass_event_list[j]._add_more_events(ass_file_line_list[row_num],
                                                          row_num, text_begin)
                row_num = simple_ass_event_list[j]._event_row[-1]

            else:
                # if the content_tuple doesn't exist
                try:
                    j = SimpleAssEvent.field_content_list.\
                        index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is new to the field_content_list
                    # then create a new SimpleAssEvent object
                    simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                      field_content_end, text_begin, field_name)
                    row_num += len(simple_ass_event._text_list)
                    simple_ass_event_list.append(simple_ass_event)
                    continue

                # if this field content is already in the field_content_list
                # then add it
                simple_ass_event_list[j]._add_more_events(ass_file_line_list[row_num],
                                                          row_num, text_begin)
                row_num = simple_ass_event_list[j]._event_row[-1]

        else:
            row_num += 1

    if len(name_tail) == len(content_tuple) and name_tail is not None:
        tail = name_tail

    else:
        tail = []

    # matched_list includes the matched ones in content_tuple
    matched_list = SimpleAssEvent.field_content_list

    for event in simple_ass_event_list:
        i = 0
        k = 0
        tail.append(event._field_content)
        if special_msg is not None:
            temp = [special_msg, ]
            temp_2 = [special_msg, ]
        else:
            temp = []
            temp_2 = []

        if is_not_text is False:
            while i < len(event._event_row) - 1:
                for line in ass_file_line_list[event._event_row[i]:event._event_row[i + 1]]:
                    for j in event._text_list:
                        temp.append(line[j:])
                i += 2

        else:
            while i < len(event._event_row) - 1:
                for line in ass_file_line_list[event._event_row[i]:event._event_row[i + 1]]:
                    for j in event._text_list:
                        temp.append(line[j:])
                        temp_2.append(line[:j + 1])
                i += 2

            fail_c, codec, is_crlf = \
                file_io.file_to_list(export_file_name + tail[k] + "_t" + ".txt", temp_2, is_forced_lf)
            if fail_c != 0:
                break

        fail_c, codec, is_crlf = \
            file_io.file_to_list(export_file_name + tail[k] + ".txt", temp, is_forced_lf)
        if fail_c != 0:
            break

        k += 1

    return matched_list, fail_c


def simple_ass_export_batch(import_dir,
                            export_dir,
                            special_msg,
                            name_tail=("_CN", "_EN"),
                            export_method=(False, False),
                            field_name="Style",
                            content_tuple=("中文字幕", "英文字幕"),
                            is_forced_lf=True
                            ):
    """Get field content from the given field name

        Params:
        import_dir          -- .ass files import direction
        export_dir          -- .ass files export direction
        special_msg         --
        name_tail           -- new files name tail tuple, ("_CN", "_EN") by default
                               if name_tail is not empty and it has the same length as the content_tuple
                               new files name will add one of these tails in order
        export_method       -- a tuple includes two Boolean Objects
                               1nd True for text-excluded content export method activated
                               otherwise it will only export text content
                               one .txt per one .ass field content
                               2rd True for changing export name into "E" + "%nd"
                               otherwise export name will stay the same
                               or add name_tail if content_tuple is not empty
        field_name          -- a field name to classify
                               ref http://moodub.free.fr/video/ass-specs.doc
        content_tuple       -- a content tuple to match, if it is None
                               it will export text grouped by field content
        is_forced_lf        -- force utf-8 without BOM and unix LF file input
                               True by default

        Return:
        fail_c              -- the count for file failure
        """

    fail_c = 0
    files_name_list = file_io.get_files_name_from_dire(import_dir)
    is_crlf = True
    for elem_name in files_name_list:
        i = 0
        temp = []
        fail_c, codec, is_crlf = \
            file_io.file_to_list(import_dir + "\\" + elem_name, temp, is_forced_lf)
        if fail_c != 0:
            break
        matched_list, fail_c = simple_ass_export_txt(temp,
                                                     export_dir + "\\" + elem_name,
                                                     special_msg, name_tail,
                                                     export_method[0], field_name, content_tuple)
        print("The result of exporting .ass file text\
        grouped by event's field: {field_n}".format(field_n=field_name))
        if len(matched_list) == 1 and len(content_tuple) != 1:
            if matched_list[0] == -1:
                print("......Section \"[Event]\" missed")
            else:
                print("......No \"{field_n}\" contents matched the field name".format(field_n=field_name))
        else:
            for has_matched in matched_list:
                print("......\"{matched}\" exported successfully".format(matched=has_matched))
            mls = set(matched_list)
            cts = set(content_tuple)
            missed_s = {x for x in cts if x not in mls}
            if len(missed_s) != 0:
                for has_missed in missed_s:
                    print("......\"{matched}\" didn't match and export".format(matched=has_missed))
        print()
        del temp
    return fail_c


def delete_ass_sect_list(ass_file_line_list,
                         sect=("[Aegisub Project Garbage]",)):
    """Delete .ass sections in ass_file_line_list from the given sect tuple.

        Params:
        ass_file_line_list       -- a target .ass file line list
        sect                     -- .ass sections name
                                    ref http://moodub.free.fr/video/ass-specs.doc

        Return:
        state_list               -- a list for deletion result in sect order
                                 -- 1 for deletion failure, 0 for deletion success
        """

    state_list = []
    for sect_e in sect:
        try:
            i = ass_file_line_list.index(sect_e)
        except ValueError:
            state_list.append(1)
            continue
        state_list.append(0)
        while i < len(ass_file_line_list):
            if ass_file_line_list[i] != "\r\n" and ass_file_line_list[i] != "\n":
                # not windows CRLF or unix LF
                del ass_file_line_list[i]
            else:
                del ass_file_line_list[i]
                break

    return state_list


def delete_ass_sect_batch(import_dir,
                          export_dir,
                          name_tail="_new",
                          sect=("[Aegisub Project Garbage]", ),
                          is_forced_lf=True):
    """Delete .ass sections in several .ass files in direction with import_dir from the given sect tuple.

        Params:
        import_dir      -- .ass files import direction
        export_dir      -- .ass files export direction
        name_tail       -- new files name tail, "_new" by default
        sect            -- .ass sections name tuple, ("[Aegisub Project Garbage]", ) by default
                           ref http://moodub.free.fr/video/ass-specs.doc
        is_forced_lf    -- force utf-8 without BOM and unix LF file input
                           True by default

        Return:
        fail_c          -- the count for file failure
        """

    fail_c = 0
    files_name_list = file_io.get_files_name_from_dire(import_dir, ".ass")
    is_crlf = True
    for elem_name in files_name_list:
        i = 0
        temp = []
        fail_c, codec, is_crlf = \
            file_io.file_to_list(import_dir + "\\" + elem_name, temp, is_forced_lf)
        if fail_c != 0:
            break
        state_list = delete_ass_sect_list(temp, sect)
        fail_c = \
            file_io.list_to_file(codec, export_dir + "\\" + elem_name + name_tail + ".ass", temp)
        if fail_c != 0:
            break
        print("The result of deleting the .ass file {elem}'s section".format(elem=elem_name))
        for is_missed in state_list:
            if is_missed:
                print("......\"{sect}\" missed".format(sect=sect[i]))
            else:
                print("......\"{sect}\" deleted successfully".format(sect=sect[i]))
            i += 1
        print()
        del temp
    return fail_c



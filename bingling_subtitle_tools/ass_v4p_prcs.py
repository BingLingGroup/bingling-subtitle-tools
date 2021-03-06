#!/usr/bin/env python
# -*- coding: utf-8 -*-
""".ass v4.00+ script format processing module
"""


# Import built-in modules
import os
import re


# Import third-party modules


# Any changes to the path and your own modules
from bingling_subtitle_tools import file_io


class GetFieldContentFailedException(Exception):
    """Failed to initialize a SimpleAssEvent class
    """

    def __init__(self):
        Exception.__init__(self)


class SimpleAssEvent:
    """Simple class for ass event section

        Reference http://moodub.free.fr/video/ass-specs.doc
        """

    simple_event_fields = ["Marked", "Start", "End", "Style", "Name",
                           "MarginL", "MarginR", "MarginV",
                           "Effect"]
    field_contents = []
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

        self.field_content = \
            event_line_list[0][field_content_begin:field_content_end]
        self.field_content_list = [field_content_begin, field_content_end, ]
        self.text_list = [first_text_begin, ]
        # save text begin position to text_list, 1 elem per line
        SimpleAssEvent.field_contents.append(self.field_content)
        # save field content to field_contents
        self.event_row = [cur_row, ]
        # save row number to event_row_list, 2 elements per part
        # part means the same field content event lines in succession
        # in the format of python slice [start:stop]
        SimpleAssEvent.field_name = field_name
        self.num = 0
        # marked the position of filter tuple

        for line in event_line_list[1:]:
            try:
                _field_content_begin, _field_content_end, _text_begin = \
                    get_field_content_and_text(line, field_name)
            except GetFieldContentFailedException:
                # the end of file or wrong format
                break
            if line.startswith("Dialogue") and self.field_content == line[_field_content_begin:_field_content_end]:
                # if field content is the same and it starts with "Dialogue"
                # then append to the list
                self.text_list.append(_text_begin)
                self.field_content_list.append(_field_content_begin)
                self.field_content_list.append(_field_content_end)
            else:
                break

        self.event_row.append(cur_row + len(self.text_list))
        # the event in the last row is not used

    def add_more_events(self,
                        event_line_list,
                        cur_row,
                        field_content_begin,
                        field_content_end,
                        first_text_begin,
                        ):
        """Initialize a SimpleAssEvent object from event_line_list

                    Params:
                    event_line_list         -- an .ass event section line list
                    cur_row                 -- current row num
                    field_content_begin     -- an .ass event field content begin pos in the first line
                    field_content_end       -- an .ass event field content end pos in the first line
                    first_text_begin        -- the text content begin pos in the first line
                    """

        _last_length = len(self.text_list)
        self.text_list.append(first_text_begin)
        self.field_content_list.append(field_content_begin)
        self.field_content_list.append(field_content_end)
        self.event_row.append(cur_row)

        for line in event_line_list[1:]:
            try:
                _field_content_begin, _field_content_end, _text_begin = \
                    get_field_content_and_text(line, SimpleAssEvent.field_name)
            except GetFieldContentFailedException:
                # the end of file or wrong format
                break
            if line.startswith("Dialogue") and self.field_content == line[_field_content_begin:_field_content_end]:
                # if field content is the same and it starts with "Dialogue"
                # then append to the list
                self.text_list.append(_text_begin)
                self.field_content_list.append(_field_content_begin)
                self.field_content_list.append(_field_content_end)
            else:
                break

        self.event_row.append(cur_row + len(self.text_list) - _last_length)
        # end in the format of a python slice end pos


# class AssV4plusStyle:
#     """Ass v4plus style section class
#
#         Reference http://moodub.free.fr/video/ass-specs.doc
#         """
#
#     def __init__(self,
#                  name="default",
#                  font_name="",
#                  font_size=0.0,
#                  primary_colour=0,
#                  secondary_colour=0,
#                  outline_colour=0,
#                  back_colour=0,
#                  bold=0,
#                  italic=0,
#                  under_line=0,
#                  strike_out=0,
#                  scale_x=0.0,
#                  scale_y=0.0,
#                  spacing=0.0,
#                  angle=0.0,
#                  border_style=0,
#                  outline=0.0,
#                  shadow=0.0,
#                  alignment=0,
#                  margin_l=0.0,
#                  margin_r=0.0,
#                  margin_v=0.0,
#                  encoding=1
#                  ):
#         self._name = name
#         # The name of the Style. Case sensitive. Cannot include commas.
#
#         self._font_name = font_name
#         # The font name as used by Windows. Case-sensitive.
#
#         self._font_size = font_size
#         # Value is float
#
#         self._primary_colour = primary_colour
#         # A long integer BGR (blue-green-red)  value. ie.
#         # the byte order in the hexadecimal equivalent of this number is BBGGRR
#         # This is the colour that a subtitle will normally appear in.
#
#         self._secondary_colour = secondary_colour
#         # A long integer BGR (blue-green-red) value. ie.
#         # the byte order in the hexadecimal equivalent of this number is BBGGRR
#         # This colour may be used instead of the Primary colour when a subtitle is automatically shifted
#         # to prevent an onscreen collision, to distinguish the different subtitles.
#
#         self._outline_colour = outline_colour
#         #  A long integer BGR (blue-green-red)  value. ie.
#         #  the byte order in the hexadecimal equivalent of this number is BBGGRR
#         #  This colour may be used instead of the Primary or Secondary colour when a subtitle is automatically shifted
#         #  to prevent an onscreen collision, to distinguish the different subtitles.
#
#         self._back_colour = back_colour
#         # This is the colour of the subtitle outline or shadow, if these are used.
#         # A long integer BGR (blue-green-red)  value. ie.
#         # the byte order in the hexadecimal equivalent of this number is BBGGRR.
#
#         self._bold = bold
#         # This defines whether text is bold (true) or not (false). -1 is True, 0 is False.
#
#         self._italic = italic
#         # This defines whether text is italic (true) or not (false). -1 is True, 0 is False.
#
#         self._under_line = under_line
#         # This defines whether text is underlined (true) or not (false). -1 is True, 0 is False.
#
#         self._strike_out = strike_out
#         # This defines whether text is strikeout (true) or not (false). -1 is True, 0 is False.
#
#         self._scale_x = scale_x
#         # Modifies the width of the font. Stays between 0.0 to 100.0 (percent)
#
#         self._scale_y = scale_y
#         # Modifies the height of the font. Stays between 0.0 to 100.0 (percent)
#
#         self._spacing = spacing
#         # Extra space between characters. Stands for pixels.
#
#         self._angle = angle
#         # The origin of the rotation is defined by the alignment. Can be a floating point number. Stands for degrees.
#
#         self._border_style = border_style
#         # 1 for outline and shadow style, 3 for opaque box style
#
#         self._outline = outline
#         # If BorderStyle is 1, then this specifies the width of the outline around the text, in pixels.
#
#         self._shadow = shadow
#         # If BorderStyle is 1, then this specifies the depth of the drop shadow behind the text, in pixels.
#         # Thick outline with shadow is not recommended.
#         # Shadow is not as effective as outline in terms of preventing an onscreen collision
#
#         self._alignment = alignment
#         # This sets how text is "justified" within the Left/Right onscreen margins, and also the vertical placing.
#         # Values stays between 1 and 9.
#         # eg. This is a screen: | 7 | 8 | 9 |
#         #                       | 4 | 5 | 6 |
#         #                       | 1 | 2 | 3 |
#         # Numbers above are values of alignment.
#
#         self._margin_l = margin_l
#         # This defines the Left Margin in pixels.
#         # It is the distance from the left-hand edge of the screen.
#         # The three onscreen margins (MarginL, MarginR, MarginV) define areas
#         # in which the subtitle text will be displayed.
#
#         self._margin_r = margin_r
#         # This defines the Right Margin in pixels.
#         # It is the distance from the right-hand edge of the screen.
#         # The three onscreen margins (MarginL, MarginR, MarginV) define areas
#         # in which the subtitle text will be displayed.
#
#         self._margin_v = margin_v
#         # This defines the vertical Left Margin in pixels.
#         # For a subtitle(alignment = 1/2/3), it is the distance from the bottom of the screen.
#         # For a toptitle(alignment = 7/8/9), it is the distance from the top of the screen.
#         # For a midtitle(alignment = 4/5/6), the value is ignored - the text will be vertically centred
#
#         self._encoding = encoding
#         # This specifies the font character set or encoding and on multi-lingual Windows installations.
#         # It provides access to characters used in multiple than one languages.
#         # It is usually 0 (zero) for English (Western, ANSI) Windows.
#         # 1 for default encoding.
#         # When the file is Unicode, this field is useful during file format conversions.


def get_field_content_and_text(line,
                               field_name="Style"):
    """Get field content and text from the given field name

        Params:
        field_name          -- the given field name, "Style" by default
                               but not "Text"

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
                # skip ":" and " "
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
        if line[field_content_end] == ",":
            field_count += 1
            break
        field_content_end += 1
        # field_content_end will stop at the next ","

    text_begin = field_content_end

    while field_content_begin < len(line) and field_count < len(SimpleAssEvent.simple_event_fields):
        if line[text_begin] == ",":
            field_count += 1
        text_begin += 1
        # text_begin will stop at the text's first char

    if text_begin == len(line):
        raise GetFieldContentFailedException

    return field_content_begin, field_content_end, text_begin


def simple_ass_export(ass_file_line_list,
                      export_file_name,
                      custom_msg,
                      out_codec,
                      ass_temp_str=None,
                      name_tail=("_CN", "_EN"),
                      filter_=("中文字幕", "英文字幕"),
                      mod_filter=None,
                      field_name="Style",
                      export_method=(True, True, False, False,
                                     False, False, True, True)
                      ):
    """Get field content from the given field name

        Params:
        ass_file_line_list  -- an .ass file line list
        export_file_name    -- export file name
        custom_msg          -- a special message is written on the first line of the files
                               None for nothing to write
        out_codec           -- the output file codec
        name_tail           -- new files name tail tuple, ("_CN", "_EN") by default
                               if name_tail is not empty and it has the same length as the filter_
                               new files name will add one of these tails in order
                               otherwise the tail will be the field content
        filter_             -- a content tuple to filter, if it is None or a zero-length tuple
                               it will export text grouped by field content
        mod_filter          -- a content tuple to change the output field content
                               in the order of the elements given by the filter_
        field_name          -- a field name to classify
                               Reference http://moodub.free.fr/video/ass-specs.doc
        export_method       -- a tuple includes 3 Boolean Objects
                               1st True for forcing utf-8 without BOM and unix LF file input
                               or it will use the same encoding
                               as the input file with the windows CRLF
                               2nd True for exporting into txt content
                               3rd True for exporting into .ass format
                               4th True for exporting extra text-excluded content
                               one .txt per one .ass field content
                               5th True for no text export
                               6th True for Keeping the override codes
                               7th True for exporting extra file
                               which combines the events all together
                               8th True for no separated events output

        Return:
        result_list         -- a list for the ones in filter_
                               filter the events
                               if filter_ is empty or None,
                               result_list will contains all of the field contents
                               [-1, ] for event section miss
                               [-2, ] for field content not match the filter_
        fail_c              -- the count for file failure
        """

    fail_c = 0

    simple_ass_event = None

    ass_head_str = None

    try:
        row_num = ass_file_line_list.index("[Events]")
    except ValueError:
        # can't find event section: return [-1, ]
        result_list = [-1, ]
        return result_list, fail_c

    if mod_filter and len(mod_filter) != len(filter_):
        mod_filter = None

    row_num += 2
    j = 0

    if export_method[2]:
        # if exporting into .ass, get the head
        if ass_temp_str:
            ass_head_str = ass_temp_str

        else:
            if export_method[0]:
                ass_head_str = "\n".join(ass_file_line_list[0:row_num]) + "\n"
            else:
                ass_head_str = "\r\n".join(ass_file_line_list[0:row_num]) + "\r\n"

    while row_num < len(ass_file_line_list):
        if ass_file_line_list[row_num].startswith("Dialogue"):
            try:
                field_content_begin, field_content_end, text_begin = \
                    get_field_content_and_text(ass_file_line_list[row_num])
            except GetFieldContentFailedException:
                # if it can't find the field content, then try the next line
                row_num += 1
                continue

            if filter_ and len(filter_) > 0:
                # first match the filter_
                try:
                    j = filter_.index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is not in the filter_, then try the next line
                    row_num += 1
                    continue

            # if the filter_ doesn't exist
            # or we want to add the field content
            # we will create a new SimpleAssEvent object
            simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                              field_content_end, text_begin, field_name)
            simple_ass_event.num = j
            row_num = simple_ass_event.event_row[-1]
            break

        else:
            # find first elem in simple_ass_event_list
            row_num += 1

    if simple_ass_event:
        simple_ass_event_list = [simple_ass_event, ]
    else:
        # can't find any event that matched the field content: return [-2, ]
        result_list = [-2, ]
        return result_list, fail_c

    while row_num < len(ass_file_line_list):
        if ass_file_line_list[row_num].startswith("Dialogue"):
            try:
                field_content_begin, field_content_end, text_begin = \
                    get_field_content_and_text(ass_file_line_list[row_num])
            except GetFieldContentFailedException:
                # if it can't find the field content, then try the next line
                row_num += 1
                continue

            if filter_ and len(filter_) > 0:
                # first match the filter_
                try:
                    j = filter_.index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is not in the filter_, then try the next line
                    row_num += 1
                    continue

                try:
                    i = SimpleAssEvent.field_contents.index(filter_[j])
                except ValueError:
                    # if this field content is new to the field_contents
                    # then create a new SimpleAssEvent object
                    simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                      field_content_end, text_begin, field_name)
                    simple_ass_event.num = j
                    row_num += len(simple_ass_event.text_list)
                    simple_ass_event_list.append(simple_ass_event)
                    continue

                # if this field content is already in the field_contents
                # then add it
                simple_ass_event_list[i].add_more_events(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                         field_content_end, text_begin)
                row_num = simple_ass_event_list[i].event_row[-1]

            else:
                # if the filter_ doesn't exist
                try:
                    i = SimpleAssEvent.field_contents.\
                        index(ass_file_line_list[row_num][field_content_begin:field_content_end])
                except ValueError:
                    # if this field content is new to the field_contents
                    # then create a new SimpleAssEvent object
                    simple_ass_event = SimpleAssEvent(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                      field_content_end, text_begin, field_name)
                    row_num += len(simple_ass_event.text_list)
                    simple_ass_event_list.append(simple_ass_event)
                    continue

                # if this field content is already in the field_contents
                # then add it
                simple_ass_event_list[i].add_more_events(ass_file_line_list[row_num:], row_num, field_content_begin,
                                                         field_content_end, text_begin)
                row_num = simple_ass_event_list[i].event_row[-1]

        else:
            row_num += 1

    if filter_ and name_tail:
        if len(name_tail) == len(filter_):
            tail = list(name_tail)
            te_tail = "_t"
        elif len(name_tail) == len(filter_) + 1:
            tail = list(name_tail)
            te_tail = name_tail[-1]
        else:
            tail = []
            te_tail = "_t"
    else:
        tail = []
        te_tail = "_t"

    if filter_ and len(filter_) > 0:
        event_zip = zip(SimpleAssEvent.field_contents, simple_ass_event_list)
        # keep the same order as content tuple
        sorted_event_zip = sorted(event_zip, key=lambda item: item[1].num)
        # result_list contains the result
        result_list, sorted_event_list = map(lambda item: list(item), zip(*sorted_event_zip))

    else:
        sorted_event_list = simple_ass_event_list
        result_list = SimpleAssEvent.field_contents

    k = 0
    if not export_method[2] and not export_method[3]:
        # export only text content into txt
        text_comb = ""
        for event in sorted_event_list:
            j = 0
            # j for event.event_row‘s row index
            i = 0
            # i for event.text_list's column index
            tail.append("_" + event.field_content)
            text = ""
            while j < len(event.event_row) - 1:
                for line in ass_file_line_list[event.event_row[j]:event.event_row[j + 1]]:
                    # traverse every part of the event
                    if not export_method[5]:
                        # don't keep override code
                        text += "".join(re.compile(r'{.*?}').split(line[event.text_list[i] + 1:]))
                    else:
                        # get every event's text
                        text += line[event.text_list[i] + 1:]
                    if export_method[0]:
                        # unix LF
                        text += "\n"
                    else:
                        # windows CRLF
                        text += "\r\n"
                    i += 1
                    # get next text column value

                j += 2
                # get next [start:stop] values of event part

            if export_method[6]:
                # need to combine
                if mod_filter:
                    text_comb = text_comb + mod_filter[k] + "\n"
                text_comb = text_comb + text

            if not export_method[7]:
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".txt", custom_msg + text,
                                        export_method[0])
            # export into txt
            k += 1

        if export_method[6]:
            # export combination into txt
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".txt", custom_msg + text_comb,
                                    export_method[0])

    elif export_method[4]:
        # export only text-excluded content
        text_ex_comb = ""
        for event in sorted_event_list:
            j = 0
            # j for event.event_row‘s row index
            i = 0
            # i for event.text_list's column index
            tail.append("_" + event.field_content)
            text_excluded = ""
            while j < len(event.event_row) - 1:
                for line in ass_file_line_list[event.event_row[j]:event.event_row[j + 1]]:
                    # get the content which excludes the text
                    if mod_filter:
                        line = line[:event.field_content_list[2 * i]] + mod_filter[k] \
                               + line[event.field_content_list[2 * i + 1]:]
                    text_excluded += line[:event.text_list[i] + 1]
                    if export_method[0]:
                        # unix LF
                        text_excluded += "\n"
                    else:
                        # windows CRLF
                        text_excluded += "\r\n"
                    i += 1

                j += 2

            if export_method[6]:
                # need to combine
                if export_method[2] and mod_filter:
                    line = ass_file_line_list[event.event_row[0]:event.event_row[1]][0]
                    line = line[:event.field_content_list[0]] + mod_filter[k] \
                        + line[event.field_content_list[1]:event.text_list[0] + 1]
                    line = line.replace("Dialogue:", "Comment:", 1) + mod_filter[k] + "\n"
                    text_ex_comb = text_ex_comb + line
                text_ex_comb = text_ex_comb + text_excluded

            if not export_method[7]:
                if export_method[1]:
                    # export into txt
                    fail_c += \
                        file_io.str_to_file(out_codec, export_file_name + tail[k] + te_tail + ".txt",
                                            custom_msg + text_excluded,  export_method[0])

                if export_method[2]:
                    # export into .ass
                    text_excluded = ass_head_str + text_excluded
                    fail_c += \
                        file_io.str_to_file(out_codec, export_file_name + tail[k] + te_tail + ".ass",
                                            custom_msg + text_excluded, export_method[0])
            k += 1

        if export_method[6]:
            # export combination into txt
            if export_method[1]:
                # export into txt
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + te_tail + ".txt", custom_msg + text_ex_comb,
                                        export_method[0])
            if export_method[2]:
                # export combination into .ass
                text_ex_comb = ass_head_str + text_ex_comb
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + te_tail + ".ass", custom_msg + text_ex_comb,
                                        export_method[0])

    elif not export_method[2]:
        # export only into txt including text-excluded content
        text_ex_comb = ""
        text_comb = ""
        for event in sorted_event_list:
            j = 0
            # j for event.event_row‘s row index
            i = 0
            # i for event.text_list's column index
            tail.append("_" + event.field_content)
            text = ""
            text_excluded = ""
            while j < len(event.event_row) - 1:
                for line in ass_file_line_list[event.event_row[j]:event.event_row[j + 1]]:
                    # get the content which excludes the text
                    if not export_method[5]:
                        # don't keep override code
                        text += "".join(re.compile(r'{.*?}').split(line[event.text_list[i] + 1:]))
                    else:
                        text += line[event.text_list[i] + 1:]
                    if mod_filter:
                        line = line[:event.field_content_list[2 * i]] + mod_filter[k] \
                               + line[event.field_content_list[2 * i + 1]:]
                    text_excluded += line[:event.text_list[i] + 1]
                    if export_method[0]:
                        # unix LF
                        text += "\n"
                        text_excluded += "\n"
                    else:
                        # windows CRLF
                        text += "\r\n"
                        text_excluded += "\r\n"
                    i += 1

                j += 2

            if export_method[6]:
                # need to combine
                if mod_filter:
                    text_comb = text_comb + mod_filter[k] + "\n"
                text_comb = text_comb + text
                text_ex_comb = text_ex_comb + text_excluded

            if not export_method[7]:
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + te_tail + ".txt",
                                        custom_msg + text_excluded, export_method[0])
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".txt", custom_msg + text, export_method[0])
                # export into txt

            k += 1

        if export_method[6]:
            # export combination into txt
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + te_tail + ".txt",
                                    custom_msg + text_ex_comb, export_method[0])
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".txt",
                                    custom_msg + text_comb, export_method[0])

    elif not export_method[3]:
        # export into txt and .ass without extra text-excluded content
        text_comb = ""
        event_ln_comb = ""
        for event in sorted_event_list:
            j = 0
            # j for event.event_row‘s row index
            i = 0
            # i for event.text_list's column index
            tail.append("_" + event.field_content)
            text = ""
            event_line = ""

            while j < len(event.event_row) - 1:
                for line in ass_file_line_list[event.event_row[j]:event.event_row[j + 1]]:
                    # get the content which excludes the text
                    if not export_method[5]:
                        # don't keep override code
                        text += "".join(re.compile(r'{.*?}').split(line[event.text_list[i] + 1:]))
                    else:
                        text += line[event.text_list[i] + 1:]
                    if mod_filter:
                        line = line[:event.field_content_list[2 * i]] + mod_filter[k] \
                               + line[event.field_content_list[2 * i + 1]:]
                    event_line += line
                    if export_method[0]:
                        # unix LF
                        text += "\n"
                        event_line += "\n"
                    else:
                        # windows CRLF
                        text += "\r\n"
                        event_line += "\r\n"
                    i += 1

                j += 2

            if export_method[6]:
                # need to combine
                if mod_filter:
                    text_comb = text_comb + mod_filter[k] + "\n"
                    line = ass_file_line_list[event.event_row[0]:event.event_row[1]][0]
                    line = line[:event.field_content_list[0]] + mod_filter[k] \
                        + line[event.field_content_list[1]:event.text_list[0] + 1]
                    line = line.replace("Dialogue:", "Comment:", 1) + mod_filter[k] + "\n"
                    event_ln_comb = event_ln_comb + line
                text_comb = text_comb + text
                event_ln_comb = event_ln_comb + event_line

            if not export_method[7]:
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".txt",
                                        custom_msg + text, export_method[0])
                # export into txt

                event_line = ass_head_str + event_line
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".ass",
                                        event_line, export_method[0])
            # export into .ass
            k += 1

        if export_method[6]:
            # export combination into txt
            # export into txt
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".txt",
                                    custom_msg + text_comb, export_method[0])
            # export combination into .ass
            event_ln_comb = ass_head_str + event_ln_comb
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".ass",
                                    event_ln_comb, export_method[0])

    else:
        # export into txt and .ass with extra text-excluded content
        text_comb = ""
        text_ex_comb = ""
        event_ln_comb = ""
        for event in sorted_event_list:
            j = 0
            # j for event.event_row‘s row index
            i = 0
            # i for event.text_list's column index
            tail.append("_" + event.field_content)
            text = ""
            text_excluded = ""
            event_line = ""
            while j < len(event.event_row) - 1:
                for line in ass_file_line_list[event.event_row[j]:event.event_row[j + 1]]:
                    # get the content which excludes the text
                    if not export_method[5]:
                        # don't keep override code
                        text += "".join(re.compile(r'{.*?}').split(line[event.text_list[i] + 1:]))
                    else:
                        text += line[event.text_list[i] + 1:]
                    if mod_filter:
                        line = line[:event.field_content_list[2 * i]] + mod_filter[k] \
                               + line[event.field_content_list[2 * i + 1]:]
                    text_excluded += line[:event.text_list[i] + 1]
                    event_line += line
                    if export_method[0]:
                        # unix LF
                        text += "\n"
                        text_excluded += "\n"
                        event_line += "\n"
                    else:
                        # windows CRLF
                        text += "\r\n"
                        text_excluded += "\r\n"
                        event_line += "\r\n"
                    i += 1

                j += 2

            if export_method[6]:
                # need to combine
                if mod_filter:
                    text_comb = text_comb + mod_filter[k] + "\n"
                    line = ass_file_line_list[event.event_row[0]:event.event_row[1]][0]
                    line = line[:event.field_content_list[0]] + mod_filter[k] \
                        + line[event.field_content_list[1]:event.text_list[0] + 1]
                    line = line.replace("Dialogue:", "Comment:", 1) + mod_filter[k] + "\n"
                    event_ln_comb = event_ln_comb + line
                    text_ex_comb = text_ex_comb + line
                text_comb = text_comb + text
                text_ex_comb = text_ex_comb + text_excluded
                event_ln_comb = event_ln_comb + event_line

            if not export_method[7]:
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + te_tail + ".txt",
                                        custom_msg + text_excluded, export_method[0])
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".txt", custom_msg + text, export_method[0])
                # export into txt

                event_line = ass_head_str + event_line
                text_excluded = ass_head_str + text_excluded

                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + te_tail + ".ass",
                                        text_excluded, export_method[0])
                fail_c += \
                    file_io.str_to_file(out_codec, export_file_name + tail[k] + ".ass",
                                        event_line, export_method[0])
            # export into .ass
            k += 1

        if export_method[6]:
            # export combination into txt
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + te_tail + ".txt",
                                    custom_msg + text_ex_comb, export_method[0])
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".txt",
                                    custom_msg + text_comb, export_method[0])
            # export combination into txt
            event_ln_comb = ass_head_str + event_ln_comb
            text_ex_comb = ass_head_str + text_ex_comb

            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + te_tail + ".ass",
                                    text_ex_comb, export_method[0])
            fail_c += \
                file_io.str_to_file(out_codec, export_file_name + ".ass",
                                    event_ln_comb, export_method[0])

    SimpleAssEvent.field_contents.clear()
    SimpleAssEvent.field_name = None
    return result_list, fail_c


def simple_ass_export_batch(import_dir,
                            export_dir,
                            custom_msg,
                            ass_temp=None,
                            field_name="Style",
                            name_tail=("_CN", "_EN"),
                            filter_=("中文字幕", "英文字幕"),
                            mod_filter=None,
                            export_method=(True, True, False, False,
                                           True, False, False, True,
                                           True)
                            ):
    """Do a batch job on exporting .ass files to txt files.

        Params:
        import_dir          -- .ass files import direction
        export_dir          -- .ass files export direction
        ass_temp            -- Another .ass file provide a template head to
                               replace the input .ass file(s) content except the events.
        custom_msg          -- a special message is written on the first line of the files
                               None for nothing to write
        field_name          -- a field name to classify
                               Reference http://moodub.free.fr/video/ass-specs.doc
        name_tail           -- new files name tail tuple, ("_CN", "_EN") by default
                               if name_tail is not empty and it has the same length as the filter_
                               new files name will add one of these tails in order
        filter_             -- a content tuple to match, if it is None or a zero-length tuple
                               it will export text grouped by field content
        mod_filter          -- a content tuple to change the output field content
                               in the order of the elements given by the filter_
        export_method       -- a tuple includes 6 Boolean Objects
                               1st True for forcing utf-8 without BOM and unix LF file output
                               or it will use the same encoding
                               as the input file with the windows CRLF
                               2nd True for changing export name into
                               "E" + the number already in the file name
                               otherwise export name will stay the same
                               or add name_tail if filter_ is not empty
                               3rd True for exporting into txt content
                               4th True for exporting into .ass format
                               5th True for exporting extra text-excluded content
                               one .txt per one .ass field content
                               6th True for no text export
                               7th True for Keeping the override codes
                               8th True for exporting extra file
                               which combines the events all together
                               9th True for no separated events output
        """

    fail_c = 0
    # the count for file failure
    files_name_list = file_io.get_files_name_from_dire(import_dir)

    ass_temp_list = []
    ass_temp_str = None

    if ass_temp:
        fail_t, codec, is_lf = \
            file_io.file_to_list(ass_temp, ass_temp_list, export_method[0])
        if fail_t != 0:
            print(".ass template file \"{ass_temp_n}\" don't exist. Check your argument.".format(ass_temp_n=ass_temp))
            return 1
        delete_ass_sect_list(ass_temp_list)

        try:
            row_num_head = ass_temp_list.index("[Events]") + 2
        except ValueError:
            try:
                ass_temp_list.index("[Script Info]")
            except ValueError:
                # can't find event section: return [-3, ]
                result_list = [-3, ]
                return result_list, fail_c
            try:
                ass_temp_list.index("[V4+ Styles]")
            except ValueError:
                # can't find event section: return [-3, ]
                result_list = [-3, ]
                return result_list, fail_c

            if ass_temp_list[:-1] != "":
                ass_temp_list.append("")

            ass_temp_list.append("[Events]")
            ass_temp_list.append("Format: Layer, Start, End, Style, Name, \
MarginL, MarginR, MarginV, Effect, Text")
            row_num_head = len(ass_temp_list)

        ass_temp_str = "\n".join(ass_temp_list[0:row_num_head]) + "\n"

    if len(files_name_list) == 0:
        print("This direction \"{dir}\" didn't contain any .ass file. Check your argument.".format(dir=import_dir))
        return 1
    print("The result of exporting .ass file text\
 grouped by event's field content:")
    for elem_name in files_name_list:
        temp = []
        print("...... .ass file name: \"{file_n}\"".format(file_n=elem_name))
        fail_t, codec, is_lf = \
            file_io.file_to_list(import_dir + "/" + elem_name, temp, export_method[0])
        if fail_t != 0:
            fail_c = fail_c + fail_t
            continue
        if export_method[1]:
            num_list = re.findall(r"\d+\.?\d*", elem_name)
            if num_list and len(num_list) > 0:
                elem_name = "E" + str(num_list[0])
        exp_m = [is_lf]
        exp_m.extend(export_method[2:9])
        result_list, fail_n = simple_ass_export(ass_file_line_list=temp,
                                                export_file_name=export_dir + "/" + os.path.splitext(elem_name)[0],
                                                ass_temp_str=ass_temp_str,
                                                custom_msg=custom_msg,
                                                out_codec=codec,
                                                name_tail=name_tail,
                                                filter_=filter_,
                                                mod_filter=mod_filter,
                                                field_name=field_name,
                                                export_method=exp_m
                                                )
        print("......  output file name: \"{file_n}\"".format(file_n=elem_name))
        print("......  event's field: \"{field_n}\"".format(field_n=field_name))
        if len(result_list) == 1 and type(result_list[0]) is int:
            if result_list[0] == -1:
                print("......  Section \"[Event]\" missed")
            elif result_list[0] == -2:
                print("......  No \"{field_n}\" contents matched the field name".format(field_n=field_name))
            elif result_list[0] == -3:
                print("......  .ass template file \"{ass_temp_n}\" is lack of several sections.".format(ass_temp_n=ass_temp))
                return 1
        elif not filter_ or len(filter_) == 0:
            print("......  The given \"Content Tuple\" is empty. Try to export all of the events.")
            for result in result_list:
                print("......  \"{matched}\" exported successfully".format(matched=result))
        else:
            for has_matched in result_list:
                print("......  \"{matched}\" exported successfully".format(matched=has_matched))
            mls = set(result_list)
            cts = set(filter_)
            missed_s = {x for x in cts if x not in mls}
            if len(missed_s) != 0:
                for has_missed in missed_s:
                    print("......  \"{matched}\" didn't match or exported".format(matched=has_missed))

        print()
        del temp

    print("Result: \n......{scs_c} file(s) exported successfully, {fai_c} input file(s) failed."
          .format(scs_c=len(files_name_list) - fail_c, fai_c=fail_c))
    return fail_c


def delete_ass_sect_list(ass_file_line_list,
                         sect=("[Aegisub Project Garbage]",)):
    """Delete .ass sections in ass_file_line_list from the given sect tuple.

        Params:
        ass_file_line_list       -- a target .ass file line list
        sect                     -- .ass sections name
                                    Reference http://moodub.free.fr/video/ass-specs.doc

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
        try:
            sect_end = ass_file_line_list.index("", i)
        except ValueError:
            del ass_file_line_list[i:]
            break
        del ass_file_line_list[i:sect_end + 1]

    return state_list


def delete_ass_sect_batch(import_dir,
                          export_dir,
                          name_tail="_new",
                          sect=("[Aegisub Project Garbage]", ),
                          is_forced_lf=True):
    """Do a batch job on deleting .ass files sections.

        Params:
        import_dir      -- .ass files import direction
        export_dir      -- .ass files export direction
        name_tail       -- new files name tail, "_new" by default
        sect            -- .ass sections name tuple, ("[Aegisub Project Garbage]", ) by default
                           Reference http://moodub.free.fr/video/ass-specs.doc
        is_forced_lf    -- force utf-8 without BOM and unix LF file input
                           True by default

        Return:
        fail_c          -- the count for file failure
        """

    fail_c = 0
    files_name_list = file_io.get_files_name_from_dire(import_dir, (".ass", ))
    if len(files_name_list) == 0:
        print("This direction \"{dir}\" didn't contain any .ass file. Check your argument.".format(dir=import_dir))
        return 1

    for elem_name in files_name_list:
        temp = []
        fail_c, codec, is_lf = \
            file_io.file_to_list(import_dir + "/" + elem_name, temp, is_forced_lf)
        if fail_c != 0:
            break
        state_list = delete_ass_sect_list(temp, sect)
        name = os.path.splitext(elem_name)[0]
        fail_c = \
            file_io.list_to_file(codec, export_dir + "/" + name + name_tail + ".ass", temp, is_lf)
        if fail_c != 0:
            break
        print("The result of deleting the section of an .ass file: \"{elem}\"".format(elem=name))
        i = 0
        for is_missed in state_list:
            if is_missed:
                print("......\"{sect}\" missed".format(sect=sect[i]))
            else:
                print("......\"{sect}\" deleted successfully".format(sect=sect[i]))
            i += 1
        print()
        del temp
    print("Result: \n......{scs_c} file(s) read successfully, {fai_c} file(s) failed."
          .format(scs_c=len(files_name_list) - fail_c, fai_c=fail_c))
    return fail_c



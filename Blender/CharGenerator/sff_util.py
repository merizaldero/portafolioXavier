"""
    MUGEN Toolkit for python
    Copyright (C) 2012-2016  Leif Theden

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Python/Pygame MUGEN SSF file support
====================================


This collection of classes is able to load and manipulate MUGEN SSF files in
python.  PIL is required for many loading the various formats.

Pygame support may be added in the future.

NOTE:
This library is very simple and is not optimized for use in a real-time
environment.  It exits for very simple uses.  Your mileage may vary.  Parental
discretion advised.  Not available in all areas.

leif theden, 2012-2016
"""
from construct import Struct, Int32ul, Int16ul, Int8ul, Bytes, Padding


sff1_subfile_header = Struct(
    #'sff1_subfile',
    next_subfile = Int32ul,
    length = Int32ul,
    axisx = Int16ul,
    axisy = Int16ul,
    groupno = Int16ul,
    imageno = Int16ul,
    index = Int16ul,    
    palette = Int8ul,
    padding = Padding(13)
)


sff1_subfile = Struct(
    #'sff1_subfile',
    header = sff1_subfile_header,
    image_data = Bytes( lambda ctx: ctx.header.length),
)


sff1_file = Struct(
    #'ssf1_file',
    signature=Bytes(12),
    version = Bytes(4),
    group_total = Int32ul,
    image_total = Int32ul,
    next_subfile = Int32ul,
    subfile_header_length = Int32ul,
    palette_type = Int8ul,
    reserved = Bytes( 3),
    padding = Padding(476),
    subfiles = sff1_subfile[ lambda ctx: ctx.image_total ]
)



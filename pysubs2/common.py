from collections import namedtuple
import sys

class Color(namedtuple("Color", "r g b a")):
    """8-bit RGB color with alpha channel"""
    pass # XXX add range check


PY3 = sys.version_info.major == 3

if PY3:
    text_type = str
else:
    text_type = unicode

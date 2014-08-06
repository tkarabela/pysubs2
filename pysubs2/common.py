from collections import namedtuple

class Color(namedtuple("Color", "r g b a")):
    """8-bit RGB color with alpha channel"""
    pass # XXX add range check

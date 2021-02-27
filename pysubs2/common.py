from collections import namedtuple
from typing import Union


_Color = namedtuple("Color", "r g b a")


class Color(_Color):
    """
    (r, g, b, a) namedtuple for 8-bit RGB color with alpha channel.

    All values are ints from 0 to 255.
    """
    def __new__(cls, r: int, g: int, b: int, a: int=0):
        for value in r, g, b, a:
            if value not in range(256):
                raise ValueError("Color channels must have values 0-255")

        return _Color.__new__(cls, r, g, b, a)


#: Version of the pysubs2 library.
VERSION = "1.1.0"


IntOrFloat = Union[int, float]

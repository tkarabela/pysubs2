from pysubs2 import Color
from nose.tools import assert_raises

def test_color_argument_validation():
    Color(r=0, g=0, b=0) # does not raise

    with assert_raises(ValueError):
        Color(r=0, g=0, b=256)

    with assert_raises(ValueError):
        Color(r=0, g=0, b=-1)

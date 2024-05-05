from pysubs2 import Color
import pytest


def test_color_argument_validation() -> None:
    Color(r=0, g=0, b=0)  # does not raise

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=256)

    with pytest.raises(ValueError):
        Color(r=0, g=0, b=-1)

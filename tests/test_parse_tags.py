from pysubs2 import SSAStyle
from pysubs2.formats.substation import parse_tags


def test_no_tags() -> None:
    text = "Hello, world!"
    assert parse_tags(text) == [(text, SSAStyle())]


def test_i_tag() -> None:
    text = "Hello, {\\i1}world{\\i0}!"
    assert parse_tags(text) == [("Hello, ", SSAStyle()),
                                ("world", SSAStyle(italic=True)),
                                ("!", SSAStyle())]


def test_r_tag() -> None:
    text = "{\\i1}Hello, {\\r}world!"
    assert parse_tags(text) == [("", SSAStyle()),
                                ("Hello, ", SSAStyle(italic=True)),
                                ("world!", SSAStyle())]


def test_r_named_tag() -> None:
    styles = {"other style": SSAStyle(bold=True)}
    text = "Hello, {\\rother style\\i1}world!"
    
    assert parse_tags(text, styles=styles) == \
        [("Hello, ", SSAStyle()),
         ("world!", SSAStyle(italic=True, bold=True))]


def test_drawing_tag() -> None:
    text = r"{\p1}m 0 0 l 100 0 100 100 0 100{\p0}test"

    fragments = parse_tags(text)
    assert len(fragments) == 3

    drawing_text, drawing_style = fragments[0]
    assert drawing_text == ""
    assert drawing_style.drawing is False

    drawing_text, drawing_style = fragments[1]
    assert drawing_text == "m 0 0 l 100 0 100 100 0 100"
    assert drawing_style.drawing is True

    drawing_text, drawing_style = fragments[2]
    assert drawing_text == "test"
    assert drawing_style.drawing is False


def test_no_drawing_tag() -> None:
    text = r"test{\paws}test"

    fragments = parse_tags(text)
    assert len(fragments) == 2
    for fragment_text, fragment_style in fragments:
        assert fragment_text == "test"
        assert fragment_style.drawing is False

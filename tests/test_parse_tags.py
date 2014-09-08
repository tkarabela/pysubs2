from pysubs2 import SSAStyle
from pysubs2.substation import parse_tags

def test_no_tags():
    text = "Hello, world!"
    assert parse_tags(text) == [(text, SSAStyle())]

def test_i_tag():
    text = "Hello, {\\i1}world{\\i0}!"
    assert parse_tags(text) == [("Hello, ", SSAStyle()),
                                ("world", SSAStyle(italic=True)),
                                ("!", SSAStyle())]

def test_r_tag():
    text = "{\\i1}Hello, {\\r}world!"
    assert parse_tags(text) == [("", SSAStyle()),
                                ("Hello, ", SSAStyle(italic=True)),
                                ("world!", SSAStyle())]

def test_r_named_tag():
    styles = {"other style": SSAStyle(bold=True)}
    text = "Hello, {\\rother style\\i1}world!"
    
    assert parse_tags(text, styles=styles) == \
        [("Hello, ", SSAStyle()),
         ("world!", SSAStyle(italic=True, bold=True))]

import pytest

from pysubs2 import SSAStyle


def test_repr_plain() -> None:
    ev = SSAStyle(fontname="Calibri", fontsize=36)
    ref = "<SSAStyle 36px 'Calibri'>"
    assert repr(ev) == ref


def test_repr_italic() -> None:
    ev = SSAStyle(fontname="Calibri", fontsize=36, italic=True)
    ref = "<SSAStyle 36px italic 'Calibri'>"
    assert repr(ev) == ref


def test_repr_bold_italic() -> None:
    ev = SSAStyle(fontname="Calibri", fontsize=36, italic=True, bold=True)
    ref = "<SSAStyle 36px bold italic 'Calibri'>"
    assert repr(ev) == ref


def test_repr_floatsize() -> None:
    ev = SSAStyle(fontname="Calibri", fontsize=36.499)
    ref = "<SSAStyle 36.499px 'Calibri'>"
    assert repr(ev) == ref


def test_fields() -> None:
    sty = SSAStyle()

    with pytest.warns(DeprecationWarning):
        assert sty.FIELDS == frozenset([
            "fontname", "fontsize", "primarycolor", "secondarycolor",
            "tertiarycolor", "outlinecolor", "backcolor",
            "bold", "italic", "underline", "strikeout",
            "scalex", "scaley", "spacing", "angle", "borderstyle",
            "outline", "shadow", "alignment",
            "marginl", "marginr", "marginv", "alphalevel", "encoding",

            "drawing"
        ])

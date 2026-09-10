import pytest

from pysubs2 import Alignment, Color, SSAStyle

COLOR_FIELDS = ["primarycolor", "secondarycolor", "tertiarycolor", "outlinecolor", "backcolor"]


@pytest.mark.parametrize("original", [
    SSAStyle(),
    SSAStyle(
        fontname="Calibri", fontsize=36.5,
        primarycolor=Color(1, 2, 3, 4), secondarycolor=Color(5, 6, 7, 8),
        tertiarycolor=Color(9, 10, 11, 12), outlinecolor=Color(13, 14, 15, 16),
        backcolor=Color(17, 18, 19, 20),
        bold=True, italic=True, underline=True, strikeout=True,
        scalex=120.0, scaley=80.0, spacing=1.5, angle=15.0,
        borderstyle=3, outline=3.5, shadow=1.5, alignment=Alignment.TOP_LEFT,
        marginl=20, marginr=30, marginv=40, alphalevel=1, encoding=0, drawing=True,
    ),
])
def test_copy_preserves_fields(original: SSAStyle) -> None:
    copied = original.copy()

    assert copied == original
    for name, value in original.as_dict().items():
        assert type(getattr(copied, name)) is type(value)


@pytest.mark.parametrize("color_field", COLOR_FIELDS)
@pytest.mark.parametrize("component", ["r", "g", "b", "a"])
def test_copy_colors_are_independent(color_field: str, component: str) -> None:
    original = SSAStyle()
    color = getattr(original, color_field)
    expected = Color(color.r, color.g, color.b, color.a)
    copied = original.copy()

    setattr(getattr(copied, color_field), component, (getattr(expected, component) + 1) % 256)

    assert getattr(original, color_field) == expected


@pytest.mark.parametrize("color_field", COLOR_FIELDS)
def test_as_dict_preserves_colors(color_field: str) -> None:
    style = SSAStyle()
    values = style.as_dict()

    assert isinstance(values[color_field], Color)
    values[color_field].r = 123

    assert getattr(style, color_field).r == 123


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

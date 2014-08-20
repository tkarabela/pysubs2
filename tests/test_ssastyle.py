from pysubs2 import SSAStyle

def test_repr_plain():
    ev = SSAStyle(fontname="Calibri", fontsize=36)
    ref = "<SSAStyle 36px 'Calibri'>"
    assert repr(ev) == ref

def test_repr_italic():
    ev = SSAStyle(fontname="Calibri", fontsize=36, italic=True)
    ref = "<SSAStyle 36px italic 'Calibri'>"
    assert repr(ev) == ref

def test_repr_bold_italic():
    ev = SSAStyle(fontname="Calibri", fontsize=36, italic=True, bold=True)
    ref = "<SSAStyle 36px bold italic 'Calibri'>"
    assert repr(ev) == ref

def test_repr_floatsize():
    ev = SSAStyle(fontname="Calibri", fontsize=36.499)
    ref = "<SSAStyle 36.499px 'Calibri'>"
    assert repr(ev) == ref

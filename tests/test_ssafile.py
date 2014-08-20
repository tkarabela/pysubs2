from pysubs2 import SSAFile, SSAStyle, SSAEvent, make_time

def test_repr_default():
    subs = SSAFile()
    ref = "<SSAFile with 0 events and 1 styles>"
    assert repr(subs) == ref

def test_repr_simple():
    subs = SSAFile()
    subs.append(SSAEvent(start=make_time(m=5), end=make_time(m=6)))
    subs.append(SSAEvent(start=make_time(m=125), end=make_time(m=126)))
    subs.append(SSAEvent(start=make_time(m=15), end=make_time(m=16)))
    subs.styles["style1"] = SSAStyle()
    subs.styles["style2"] = SSAStyle()
    ref = "<SSAFile with 3 events and 3 styles, last timestamp 2:06:00>"
    assert repr(subs) == ref

from pysubs2 import SSAEvent, make_time

def test_repr_dialogue():
    ev = SSAEvent(start=make_time(m=1, s=30), end=make_time(m=1, s=35), text="Hello\\Nworld!")
    ref = "<SSAEvent type=Dialogue start=0:01:30 end=0:01:35 text='Hello\\Nworld!'>"
    assert repr(ev) == ref

def test_repr_comment():
    ev = SSAEvent(start=make_time(m=1, s=30), end=make_time(m=1, s=35), text="Hello\\Nworld!")
    ev.is_comment = True
    ref = "<SSAEvent type=Comment start=0:01:30 end=0:01:35 text='Hello\\Nworld!'>"
    assert repr(ev) == ref

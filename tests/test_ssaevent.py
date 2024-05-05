import pytest

from pysubs2 import SSAEvent, make_time


def test_repr_dialogue() -> None:
    ev = SSAEvent(start=make_time(m=1, s=30), end=make_time(m=1, s=35), text="Hello\\Nworld!")
    ref = r"<SSAEvent type=Dialogue start=0:01:30 end=0:01:35 text='Hello\\Nworld!'>"
    assert repr(ev) == ref


def test_repr_comment() -> None:
    ev = SSAEvent(start=make_time(m=1, s=30), end=make_time(m=1, s=35), text="Hello\\Nworld!")
    ev.is_comment = True
    ref = r"<SSAEvent type=Comment start=0:01:30 end=0:01:35 text='Hello\\Nworld!'>"
    assert repr(ev) == ref


def test_duration() -> None:
    e = SSAEvent(start=0, end=10)
    assert e.duration == 10

    e.duration = 20
    assert e.start == 0 and e.end == 20

    e.duration = 5
    assert e.start == 0 and e.end == 5

    e.duration = 0
    assert e.start == 0 and e.end == 0

    with pytest.raises(ValueError):
        e.duration = -20


def test_plaintext() -> None:
    e = SSAEvent(text=r"First\NSecond\NThird\hline{with hidden text}")
    assert e.plaintext == "First\nSecond\nThird line"

    e.plaintext = "My\n Text "
    assert e.text == r"My\N Text "

    # SubStation has no way to escape braces, thus this wart
    text = "My text{with braces}"
    e.plaintext = text
    assert e.plaintext != text


def test_shift() -> None:
    e = SSAEvent(start=0, end=10)

    with pytest.raises(ValueError):
        e.shift(frames=5)

    with pytest.raises(ValueError):
        e.shift(fps=23.976)

    with pytest.raises(ValueError):
        e.shift(frames=5, fps=-1)

    e2 = e.copy()
    e2.shift(ms=5)
    assert e2 == SSAEvent(start=5, end=15)

    e2 = e.copy()
    e2.shift(ms=-5)
    assert e2 == SSAEvent(start=-5, end=5)

    e2 = e.copy()
    e2.shift(frames=1, fps=100.0)
    assert e2 == SSAEvent(start=10, end=20)

    e2 = e.copy()
    e2.shift(frames=-1, fps=100.0)
    assert e2 == SSAEvent(start=-10, end=0)

    e2 = e.copy()
    e2.shift(h=1, m=-60, s=2, ms=-2000)
    assert e2 == e


def test_fields() -> None:
    e = SSAEvent()
    with pytest.warns(DeprecationWarning):
        assert e.FIELDS == frozenset([
            "start", "end", "text", "marked", "layer", "style",
            "name", "marginl", "marginr", "marginv", "effect", "type"
        ])

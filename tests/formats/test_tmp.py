"""
pysubs2.formats.tmp tests

"""

from textwrap import dedent
import pytest

from pysubs2 import SSAFile, SSAEvent, make_time
from pysubs2.formats.tmp import MAX_REPRESENTABLE_TIME


def test_simple_write() -> None:
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = "ten--chars"

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "ten--chars-ten-chars"

    e3 = SSAEvent()
    e3.start = 60000
    e3.end = 120000
    e3.text = "Invisible subtitle."
    e3.is_comment = True

    subs.append(e1)
    subs.append(e2)
    subs.append(e3)

    ref = dedent("""\
    00:00:00:ten--chars
    00:01:00:ten--chars-ten-chars
    """)

    text = subs.to_string("tmp")
    assert text.strip() == ref.strip()


def test_simple_read() -> None:
    text = dedent("""\
    00:00:00:ten--chars
    00:01:00:ten--chars-ten-chars
    """)
    #calculate endtime from starttime + 500 miliseconds + 67 miliseconds per each character (15 chars per second)
    ref = SSAFile()
    ref.append(SSAEvent(start=0, end=make_time(ms=1840), text="ten--chars"))
    ref.append(SSAEvent(start=make_time(m=1), end=make_time(ms=62510), text="ten--chars-ten-chars"))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)


def test_overlapping_read() -> None:
    # see issue #35
    text = dedent("""\
    00:00:12:I ... this is some long text ... ... this is some long text ...
    00:00:14:observing ... ... this is some long text ... ... this is some long text ...
    00:00:18:and ... ... this is some long text ... ... this is some long text ...
    00:00:22:You ... ... this is some long text ... ... this is some long text ...
    """)
    subs = SSAFile.from_string(text)
    assert subs[0].start == make_time(s=12)
    assert subs[0].end == subs[1].start == make_time(s=14)
    assert subs[1].end == subs[2].start == make_time(s=18)
    assert subs[2].end == subs[3].start == make_time(s=22)


def test_styled_read() -> None:
    text = dedent("""\
    00:00:00:ten--chars--<u>underline</u>
    00:01:00:ten--chars--<b><xxx>some--tags</xxx></b>
    """)

    subs = SSAFile.from_string(text)
    assert subs[0].text == r"ten--chars--{\u1}underline"
    assert subs[1].text == "ten--chars--some--tags"


def test_write_drawing() -> None:
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = r"{\p1}m 0 0 l 100 0 100 100 0 100{\p0}test"

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "ten--chars-ten-chars"

    e3 = SSAEvent()
    e3.start = 60000
    e3.end = 120000
    e3.text = "Invisible subtitle."
    e3.is_comment = True

    subs.append(e1)
    subs.append(e2)
    subs.append(e3)

    ref = dedent("""\
    00:01:00:ten--chars-ten-chars
    """)

    text = subs.to_string("tmp")
    assert text.strip() == ref.strip()


def test_overflow_timestamp_write() -> None:
    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(h=1000), end=make_time(h=1001), text="test"))
    with pytest.warns(RuntimeWarning):
        text = ref.to_string("tmp")
    subs = SSAFile.from_string(text)
    assert subs[0].start == MAX_REPRESENTABLE_TIME

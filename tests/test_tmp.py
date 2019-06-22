"""
pysubs2.formats.tmp tests

"""

from __future__ import unicode_literals
from textwrap import dedent
from pysubs2 import SSAFile, SSAEvent, make_time

def test_simple_write():
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


def test_simple_read():
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




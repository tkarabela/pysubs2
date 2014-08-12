"""
pysubs2.formats.subrip tests

"""

from __future__ import unicode_literals
from textwrap import dedent
from pysubs2 import SSAFile, SSAEvent, make_time

def test_simple_write():
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = "An example subtitle."

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "Subtitle number\\Ntwo."

    e3 = SSAEvent()
    e3.start = 60000
    e3.end = 120000
    e3.text = "Invisible subtitle."
    e3.is_comment = True

    subs.append(e1)
    subs.append(e2)
    subs.append(e3)

    ref = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    An example subtitle.

    2
    00:01:00,000 --> 00:02:00,000
    Subtitle number
    two.
    """)

    text = subs.to_string("srt")
    assert text.strip() == ref.strip()


def test_simple_read():
    text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    An example subtitle.

    2
    00:01:00,000 --> 00:02:00,000
    Subtitle number
    two.
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=0, end=make_time(m=1), text="An example subtitle."))
    ref.append(SSAEvent(start=make_time(m=1), end=make_time(m=2), text="Subtitle number\\Ntwo."))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

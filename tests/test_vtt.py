"""
pysubs2.formats.vtt tests

"""

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
    WEBVTT
    
    1
    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.
    """)

    text = subs.to_string("vtt")
    assert text.strip() == ref.strip()

def test_writes_in_time_order():
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = "An example subtitle."

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "Subtitle number\\Ntwo."

    subs.append(e2)
    subs.append(e1)

    ref = dedent("""\
    WEBVTT
    
    1
    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.
    """)

    text = subs.to_string("vtt")
    assert text.strip() == ref.strip()

def test_simple_read():
    text = dedent("""\
    WEBVTT
    
    1
    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=0, end=make_time(m=1), text="An example subtitle."))
    ref.append(SSAEvent(start=make_time(m=1), end=make_time(m=2), text="Subtitle number\\Ntwo."))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

def test_read_complex():
    # regression test for #30
    text = dedent("""\
    WEBVTT
    X-TIMESTAMP-MAP=LOCAL:00:00:00.000,MPEGTS:0
    
    00:50.099 --> 00:53.299 line:85% align:middle
    Cuidem do seu grupo.
    Cuidem de suas fileiras.
    
    01:54.255 --> 01:55.455 line:85% align:middle
    Parem!
    
    01:58.155 --> 01:59.555 line:85% align:middle
    E, parem!
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(s=50, ms=99), end=make_time(s=53, ms=299),
                        text=r"Cuidem do seu grupo.\NCuidem de suas fileiras."))
    ref.append(SSAEvent(start=make_time(m=1, s=54, ms=255), end=make_time(m=1, s=55, ms=455),
                        text="Parem!"))
    ref.append(SSAEvent(start=make_time(m=1, s=58, ms=155), end=make_time(m=1, s=59, ms=555),
                        text="E, parem!"))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

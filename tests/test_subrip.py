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

def test_read_malformed():
    """no line number, no empty line, leading whitespace, bad timestamp format"""

    text = dedent("""\
    00:00:00.000 ->00:01:00.000
    An example subtitle.
         0:01:00,00 --> 0:02:00,00
         Subtitle number
    two.
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=0, end=make_time(m=1), text="An example subtitle."))
    ref.append(SSAEvent(start=make_time(m=1), end=make_time(m=2), text="Subtitle number\\Ntwo."))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

def test_read_position_styling():
    """position is ignored, italic is converted, color is ignored"""

    text = dedent("""\
    1
    00:00:10,500 --> 00:00:13,000  X1:63 X2:223 Y1:43 Y2:58
    <i>Elephant's Dream</i>

    2
    00:00:15,000 --> 00:00:18,000  X1:53 X2:303 Y1:438 Y2:453
    <font color="cyan">At the left we can see...</font>
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(s=10.5), end=make_time(s=13), text="{\\i1}Elephant's Dream{\\i0}"))
    ref.append(SSAEvent(start=make_time(s=15), end=make_time(s=18), text="At the left we can see..."))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

def test_read_bad_tags():
    """missing opening/closing tag, bad nesting, extra whitespace"""

    text = dedent("""\
    1
    00:00:10,500 --> 00:00:13,000
    < u><i><font color="red" >Elephant's < s>Dream< /  i > Is Long</s> And Badly Nested</xyz>

    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(s=10.5), end=make_time(s=13), text="{\\u1}{\\i1}Elephant's {\\s1}Dream{\\i0} Is Long{\\s0} And Badly Nested"))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

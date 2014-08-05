"""
pysubs2.formats.subrip tests

"""

from __future__ import unicode_literals
from textwrap import dedent
import pysubs2

def test_simple():
    subs = pysubs2.SSAFile()

    e1 = pysubs2.SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = "An example subtitle."

    e2 = pysubs2.SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "Subtitle number two."

    e3 = pysubs2.SSAEvent()
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
    Subtitle number two.
    """)

    text = subs.to_string("srt")

    assert text.strip() == ref.strip()

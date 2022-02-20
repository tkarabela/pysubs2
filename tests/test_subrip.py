"""
pysubs2.formats.subrip tests

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

def test_empty_subtitles():
    # regression test for issue #11

    text = dedent("""
    392
    00:29:27,46 --> 00:29:29,83
    I'm Liza Minnelli..

    393
    00:00:00,00 --> 00:00:00,00

    394
    00:00:00,00 --> 00:00:00,00
    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(m=29, s=27, ms=460), end=make_time(m=29, s=29, ms=830), text="I'm Liza Minnelli.."))
    ref.append(SSAEvent(start=0, end=0, text=""))
    ref.append(SSAEvent(start=0, end=0, text=""))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)

def test_keep_unknown_html_tags():
    # see issue #26
    text = dedent("""\
        1
        00:00:10,500 --> 00:00:13,000
        <i>Elephant's <sub>Little</sub> Dream</i>

        2
        00:00:15,000 --> 00:00:18,000
        <font color="cyan">At the left we can see...</font>
        """)

    ref_default = SSAFile()
    ref_default.append(SSAEvent(start=make_time(s=10.5), end=make_time(s=13), text="{\\i1}Elephant's Little Dream{\\i0}"))
    ref_default.append(SSAEvent(start=make_time(s=15), end=make_time(s=18), text="At the left we can see..."))

    ref_keep = SSAFile()
    ref_keep.append(SSAEvent(start=make_time(s=10.5), end=make_time(s=13), text="{\\i1}Elephant's <sub>Little</sub> Dream{\\i0}"))
    ref_keep.append(SSAEvent(start=make_time(s=15), end=make_time(s=18), text="<font color=\"cyan\">At the left we can see...</font>"))

    subs_default = SSAFile.from_string(text)
    subs_keep = SSAFile.from_string(text, keep_unknown_html_tags=True)

    assert subs_default.equals(ref_default)
    assert subs_keep.equals(ref_keep)
    assert subs_keep.to_string("srt") == ref_keep.to_string("srt")

def test_write_drawing():
    # test for 7bde9a6c3a250cf0880a8a9fe31d1b6a69ff21a0
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = r"{\p1}m 0 0 l 100 0 100 100 0 100{\p0}test"

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "Subtitle number\\Ntwo."

    subs.append(e1)
    subs.append(e2)

    ref = dedent("""\
    1
    00:01:00,000 --> 00:02:00,000
    Subtitle number
    two.
    """)

    text = subs.to_string("srt")
    assert text.strip() == ref.strip()

def test_keep_ssa_tags():
    # test for issue #48
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    {\\an7}An example subtitle.

    2
    00:01:00,000 --> 00:02:00,000
    Subtitle {\\b1}number{\\b0}
    two.
    """)

    subs = SSAFile.from_string(input_text)

    output_text_do_not_keep_tags = subs.to_string("srt")
    output_text_keep_tags = subs.to_string("srt", keep_ssa_tags=True)

    assert input_text.strip() != output_text_do_not_keep_tags.strip()
    assert input_text.strip() == output_text_keep_tags.strip()

"""
pysubs2.formats.subrip tests

"""
import os.path as op
import tempfile
from textwrap import dedent
import pytest

from pysubs2 import SSAFile, SSAEvent, make_time
from pysubs2.formats.subrip import MAX_REPRESENTABLE_TIME


def test_simple_write() -> None:
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


def test_writes_in_given_order() -> None:
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
    1
    00:01:00,000 --> 00:02:00,000
    Subtitle number
    two.

    2
    00:00:00,000 --> 00:01:00,000
    An example subtitle.
    """)

    text = subs.to_string("srt")
    assert text.strip() == ref.strip()


def test_simple_read() -> None:
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


def test_read_malformed() -> None:
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


def test_read_position_styling() -> None:
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


def test_read_bad_tags() -> None:
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


def test_read_tags() -> None:
    text = dedent("""\
    1
    00:00:10,500 --> 00:00:13,000
    <i>italic <b>bold <u>underline <s>strikethrough</s></u></b></i>

    """)

    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(s=10.5), end=make_time(s=13), text="{\\i1}italic {\\b1}bold {\\u1}underline {\\s1}strikethrough{\\s0}{\\u0}{\\b0}{\\i0}"))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)


def test_empty_subtitles() -> None:
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


def test_keep_unknown_html_tags() -> None:
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


def test_write_drawing() -> None:
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


def test_keep_ssa_tags() -> None:
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


def test_keep_ssa_tags_and_html_tags() -> None:
    # test for issue #48
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    {\\an7}An example <i>subtitle</i>.

    2
    00:01:00,000 --> 00:02:00,000
    Subtitle {\\b1}number{\\b0}
    two.
    """)

    subs = SSAFile.from_string(input_text, keep_html_tags=True)

    output_text_do_not_keep_tags = subs.to_string("srt")
    output_text_keep_tags = subs.to_string("srt", keep_ssa_tags=True)

    assert input_text.strip() != output_text_do_not_keep_tags.strip()
    assert input_text.strip() == output_text_keep_tags.strip()


def test_overflow_timestamp_write() -> None:
    ref = SSAFile()
    ref.append(SSAEvent(start=make_time(h=1000), end=make_time(h=1001), text="test"))
    with pytest.warns(RuntimeWarning):
        text = ref.to_string("srt")
    subs = SSAFile.from_string(text)
    assert subs[0].end == MAX_REPRESENTABLE_TIME


def test_win1250_passthrough_with_surrogateescape() -> None:
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    The quick brown fox jumps over the lazy dog

    2
    00:01:00,000 --> 00:02:00,000
    Příliš žluťoučký kůň úpěl ďábelské ódy
    
    """)

    input_bytes_win1250 = input_text.encode("windows-1250")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_path = op.join(temp_dir, "output.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes_win1250)

        with pytest.raises(UnicodeDecodeError):
            SSAFile.load(input_path)

        subs = SSAFile.load(input_path, errors="surrogateescape")

        assert subs[0].text == "The quick brown fox jumps over the lazy dog"
        assert subs[1].text.startswith("P") and subs[1].text.endswith("dy")

        subs.save(output_path, errors="surrogateescape")

        with open(output_path, "rb") as fp:
            output_bytes = fp.read().replace(b"\r", b"")

        assert input_bytes_win1250 == output_bytes


def test_multiencoding_passthrough_with_surrogateescape() -> None:
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    The quick brown fox jumps over the lazy dog""")

    input_bytes = input_text.encode("ascii")
    input_bytes += b"\n" + "Příliš žluťoučký kůň úpěl ďábelské ódy".encode("windows-1250")
    input_bytes += b"\n" + "Vamp quäkt: Grüß Felix bzw. Jody schön!".encode("utf-8")
    input_bytes += b"\n" + "日本国".encode("shift-jis")
    input_bytes += b"\n" + "道德經".encode("big5")
    input_bytes += b"\n\n"

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_path = op.join(temp_dir, "output.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes)

        with pytest.raises(UnicodeDecodeError):
            SSAFile.load(input_path)

        subs = SSAFile.load(input_path, errors="surrogateescape")

        assert subs[0].text.startswith("The quick brown fox jumps over the lazy dog")
        assert "Felix bzw. Jody" in subs[0].text

        subs.save(output_path, errors="surrogateescape")

        with open(output_path, "rb") as fp:
            output_bytes = fp.read().replace(b"\r", b"")

        assert input_bytes == output_bytes


def test_utf8_read_write() -> None:
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    The quick brown fox jumps over the lazy dog
    Příliš žluťoučký kůň úpěl ďábelské ódy
    Vamp quäkt: Grüß Felix bzw. Jody schön!
    日本国
    道德經
    
    """)

    input_bytes = input_text.encode("utf-8")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_path = op.join(temp_dir, "output.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes)

        # legacy behaviour
        subs_legacy = SSAFile.load(input_path, errors=None)
        subs = SSAFile.load(input_path)
        assert subs.equals(subs_legacy)

        subs.save(output_path)

        with open(output_path, "rb") as fp:
            output_bytes = fp.read().replace(b"\r", b"")

        assert input_bytes == output_bytes


def test_win1250_read_write() -> None:
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    The quick brown fox jumps over the lazy dog
    Příliš žluťoučký kůň úpěl ďábelské ódy

    """)

    input_bytes = input_text.encode("windows-1250")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_path = op.join(temp_dir, "output.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes)

        # legacy behaviour
        subs_legacy = SSAFile.load(input_path, encoding="windows-1250", errors=None)
        subs = SSAFile.load(input_path, encoding="windows-1250")
        assert subs.equals(subs_legacy)

        subs.save(output_path, encoding="windows-1250")

        with open(output_path, "rb") as fp:
            output_bytes = fp.read().replace(b"\r", b"")

        assert input_bytes == output_bytes


def test_big5_read_write() -> None:
    input_text = dedent("""\
    1
    00:00:00,000 --> 00:01:00,000
    道德經

    """)

    input_bytes = input_text.encode("big5")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_path = op.join(temp_dir, "output.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes)

        # legacy behaviour
        subs_legacy = SSAFile.load(input_path, encoding="big5", errors=None)
        subs = SSAFile.load(input_path, encoding="big5")
        assert subs.equals(subs_legacy)

        subs.save(output_path, encoding="big5")

        with open(output_path, "rb") as fp:
            output_bytes = fp.read().replace(b"\r", b"")

        assert input_bytes == output_bytes

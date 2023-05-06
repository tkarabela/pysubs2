from textwrap import dedent
import pytest

from pysubs2 import SSAFile, SSAEvent, SSAStyle, UnknownFPSError


def test_framerate_inference():
    fps = 1000.0
    
    has_fps = dedent("""\
    {0}{0}1000.0
    {10}{20}Hello!
    """)
    
    no_fps = dedent("""\
    {10}{20}Hello!
    """)
    
    ignored_fps = dedent("""\
    {0}{0}23.976
    {10}{20}Hello!
    """)
    
    illegal_fps = dedent("""\
    {0}{0}-23.976
    {10}{20}Hello!
    """)
    
    subs1 = SSAFile.from_string(has_fps)
    assert subs1.fps == fps
    assert len(subs1) == 1
    assert subs1[0] == SSAEvent(start=10, end=21, text="Hello!")
    
    subs2 = SSAFile.from_string(no_fps, fps=fps)
    assert subs2.fps == fps
    assert len(subs2) == 1
    assert subs2[0] == SSAEvent(start=10, end=21, text="Hello!")
    
    # fps argument takes preference over what the file says, first line is kept
    subs3 = SSAFile.from_string(ignored_fps, fps=fps)
    assert subs3.fps == fps
    assert len(subs3) == 2
    assert subs3[0] == SSAEvent(start=0, end=1, text="23.976")
    assert subs3[1] == SSAEvent(start=10, end=21, text="Hello!")
    
    with pytest.raises(UnknownFPSError):
        SSAFile.from_string(no_fps)
    
    with pytest.raises(ValueError):
        SSAFile.from_string(illegal_fps)

def test_extra_whitespace_parsing():
    f = dedent("""\
    
       { 0 } { 0 }  1000.0   
    
     {    10 }{    20}   Hello!      
    
    """)
    
    subs = SSAFile.from_string(f)
    assert subs[0] == SSAEvent(start=10, end=21, text="Hello!")

def test_newlines_parsing():
    f = "{10}{20}   So|Many||Newlines |||  "
    subs = SSAFile.from_string(f, fps=1000)
    assert subs[0].text == r"So\NMany\N\NNewlines \N\N\N"

def test_tags_parsing():
    f1 = "{10}{20}{Y:i,u}Hello!"
    subs1 = SSAFile.from_string(f1, fps=1000)
    assert subs1[0].text == "{\\i1\\u1}Hello!"
    
    f2 = "{10}{20}Hello, {f:Comic Sans MS}world!"
    subs2 = SSAFile.from_string(f2, fps=1000)
    assert subs2[0].text == r"Hello, {\fnComic Sans MS}world!"

    # the C tag is not supported, unsupported tags are copied verbatim
    f3 = "{10}{20}Hello, {c:$0000FF}world!"
    subs3 = SSAFile.from_string(f3, fps=1000)
    assert subs3[0].text == r"Hello, {c:$0000FF}world!"

    f4 = "{10}{20}Hello, {P:100,200}world!"
    subs4 = SSAFile.from_string(f4, fps=1000)
    assert subs4[0].text == r"Hello, {\pos(100,200)}world!"

    f5 = "{10}{20}Hello, {s:72}world!"
    subs5 = SSAFile.from_string(f5, fps=1000)
    assert subs5[0].text == r"Hello, {\fs72}world!"

def test_parser_skipping_lines():
    f = dedent("""\
    Ook!
    
    {0}{0}23.976
    > Hi!
    {10}{20}Hello!
    1
    00:00:00,000 --> 00:00:05,000
    When editing their SRT files,
    some people get so careless
    as to paste them in their MicroDVD files!
    """)
    
    subs = SSAFile.from_string(f, format_="microdvd")
    assert len(subs) == 1
    assert subs[0].text == "Hello!"

def test_writer_tags():
    subs = SSAFile()
    subs.styles["italic_style"] = SSAStyle(italic=True)
    subs.events = [SSAEvent(start=0, end=11, text=r"Plain."),
                   SSAEvent(start=0, end=11, text=r"{\i1}Inline."),
                   SSAEvent(start=0, end=11, text=r"Styled.", style="italic_style"),
                   SSAEvent(start=0, end=11, text=r"{\i1}Also{\i0} {\ritalic_style}italic."),
                   SSAEvent(start=0, end=11, text=r"Not {\i1}italic.")]
    
    f = dedent("""\
    {0}{0}1000
    {0}{10}Plain.
    {0}{10}{Y:i}Inline.
    {0}{10}{Y:i}Styled.
    {0}{10}{Y:i}Also italic.
    {0}{10}Not italic.
    """)
    
    assert subs.to_string("microdvd", 1000) == f

def test_writer_uses_original_fps():
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=11, text="Hello!"))
    subs.fps = 1000
    
    f = dedent("""\
    {0}{0}1000
    {0}{10}Hello!
    """)
    
    assert subs.to_string("microdvd") == f

def test_writer_skips_comment_lines():
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=11, text="Hello!"))
    subs.append(SSAEvent(start=0, end=11, text="World!"))
    subs[0].is_comment = True
    
    f = dedent("""\
    {0}{0}1000
    {0}{10}World!
    """)
    
    assert subs.to_string("microdvd", fps=1000) == f

def test_writer_handles_whitespace():
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=11,
                         text=r"Hello,\hworld!\NSo many\N\nNewlines."))
    
    f = dedent("""\
    {0}{0}1000
    {0}{10}Hello, world!|So many||Newlines.
    """)
    
    assert subs.to_string("microdvd", fps=1000) == f

def test_writer_strips_tags():
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=11, text="Let me tell you{a secret}."))
    
    f = dedent("""\
    {0}{0}1000
    {0}{10}Let me tell you.
    """)
    
    assert subs.to_string("microdvd", fps=1000) == f

def test_write_drawing():
    subs = SSAFile()
    subs.append(SSAEvent(start=0, end=10, text=r"{\p1}m 0 0 l 100 0 100 100 0 100{\p0}test"))
    subs.append(SSAEvent(start=10, end=20, text="Let me tell you."))

    f = dedent("""\
    {0}{0}1000
    {10}{19}Let me tell you.
    """)

    assert subs.to_string("microdvd", fps=1000) == f

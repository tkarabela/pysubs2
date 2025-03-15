"""
pysubs2.formats.vtt tests

"""

from textwrap import dedent

from pysubs2 import SSAFile, SSAEvent, make_time


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
    e3.text = "NOTE Invisible subtitle."
    e3.is_comment = True

    subs.info["VTTHeaderText"] = "A header with text."
    subs.append(e1)
    subs.append(e2)
    subs.append(e3)

    ref = dedent("""\
    WEBVTT A header with text.

    1
    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.

    NOTE Invisible subtitle.
    """)

    text = subs.to_string("vtt", cue_with_identifier=True, blank_lines_between_blocks=1, reorder_cues_by_time=False)
    assert text.strip() == ref.strip()


def test_complex_write() -> None:
    subs = SSAFile()

    subs.info["VTTHeaderText"] = "A header with text."
    subs.info["VTTXTimestampMap"] = "LOCAL:00:00:00.000,MPEGTS:0"
    subs.append(SSAEvent(start=0, end=make_time(m=1),
                         text="An example subtitle."))
    subs.append(SSAEvent(start=make_time(m=1), end=make_time(m=2),
                         text=r"Subtitle number\Ntwo."))
    subs.append(SSAEvent(start=make_time(m=2, s=0, ms=100), end=make_time(m=2, s=7, ms=342),
                         text=r'{\N"type": "WikipediaPage",\N"url": "https://en.wikipedia.org/wiki/Samurai_Pizza_Cats"\N}',
                         vtt_cue_about={"identifier": "wikipage"}))
    subs.append(SSAEvent(start=make_time(m=2, s=0, ms=110), end=make_time(m=2, s=0, ms=120),
                         text="NOTE Invisible subtitle.",
                         type="Comment", vtt_cue_about={"identifier": "isnrs"}))

    ref = dedent("""\
    WEBVTT A header with text.
    X-TIMESTAMP-MAP=LOCAL:00:00:00.000,MPEGTS:0


    00:00:00.000 --> 00:01:00.000
    An example subtitle.


    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.


    wikipage
    00:02:00.100 --> 00:02:07.342
    {
    "type": "WikipediaPage",
    "url": "https://en.wikipedia.org/wiki/Samurai_Pizza_Cats"
    }


    NOTE Invisible subtitle.
    """)

    text = subs.to_string("vtt", cue_with_identifier=True, blank_lines_between_blocks=2)
    assert text.strip() == ref.strip()



def test_write_no_identifier() -> None:
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = "An example subtitle."

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = "Subtitle number\\Ntwo."

    subs.append(e1)
    subs.append(e2)

    ref = dedent("""\
    WEBVTT

    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.
    """)

    text = subs.to_string("vtt", cue_with_identifier=False, blank_lines_between_blocks=1)
    assert text.strip() == ref.strip()


def test_writes_in_time_order() -> None:
    subs = SSAFile()

    e1 = SSAEvent()
    e1.start = 0
    e1.end = 60000
    e1.text = r"{\u1}An example subtitle.{\u0}"
    e1.vtt_cue_about = {"setting": {"line": "85%", "align": "middle"}}

    e2 = SSAEvent()
    e2.start = 60000
    e2.end = 120000
    e2.text = r"Subtitle number\N{\b1}two."

    e3 = SSAEvent()
    e3.start = 150000
    e3.end = 200000
    e3.text = r"{\i1}Subtitle number\Nthree."

    subs.append(e3)
    subs.append(e2)
    subs.append(e1)

    ref = dedent("""\
    WEBVTT

    1
    00:00:00.000 --> 00:01:00.000 line:85% align:middle
    <u>An example subtitle.</u>

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    <b>two.</b>

    3
    00:02:30.000 --> 00:03:20.000
    <i>Subtitle number
    three.</i>
    """)

    text = subs.to_string("vtt", cue_with_identifier=True, reorder_cues_by_time=True, blank_lines_between_blocks=1)
    assert text.strip() == ref.strip()


def test_simple_read() -> None:
    text = dedent("""\
    WEBVTT hello world
    
    1 my text
    00:00:00.000 --> 00:01:00.000
    An example subtitle.

    2
    00:01:00.000 --> 00:02:00.000
    Subtitle number
    two.
    """)

    ref = SSAFile()
    ref.info["VTTHeaderText"] = "hello world"
    ref.append(
        SSAEvent(start=0, end=make_time(m=1), text="An example subtitle.", vtt_cue_about={"identifier": "1 my text"}))
    ref.append(SSAEvent(start=make_time(m=1), end=make_time(m=2), text="Subtitle number\\Ntwo.",
                        vtt_cue_about={"identifier": "2"}))

    subs = SSAFile.from_string(text)
    assert subs.equals(ref)


def test_read_complex() -> None:
    # regression test for #30
    text = dedent("""\
    WEBVTT
    X-TIMESTAMP-MAP=LOCAL:00:00:00.000,MPEGTS:0

    NOTE This is a single line comment

    00:50.099 --> 00:53.299 line:85% align:middle
    <b>Cuidem do seu grupo.</b>
    Cuidem de suas fileiras.
    
    01:54.255 --> 01:55.455 line:85% align:middle
    <i>Parem!</i>
    
    01:58.155 --> 01:59.555 line:85% align:middle
    E, parem!

    01:59.100 --> 01:59.342

    02:00.100 --> 02:07.342
    {
    "type": "WikipediaPage",
    "url": "https://en.wikipedia.org/wiki/Samurai_Pizza_Cats"
    }

    NOTE I might add a line to indicate work that still has to be done.
    """)

    ref = SSAFile()
    ref.info["VTTXTimestampMap"] = "LOCAL:00:00:00.000,MPEGTS:0"
    ref.append(SSAEvent(start=make_time(s=50, ms=89), end=make_time(s=50, ms=99),
                        text="NOTE This is a single line comment",
                        type="Comment",
                        vtt_cue_about={'identifier': 'isnrs'}))
    ref.append(SSAEvent(start=make_time(s=50, ms=99), end=make_time(s=53, ms=299),
                        text=r"{\b1}Cuidem do seu grupo.{\b0}\NCuidem de suas fileiras.",
                        vtt_cue_about={"setting": {"line": "85%", "align": "middle"}}))
    ref.append(SSAEvent(start=make_time(m=1, s=54, ms=255), end=make_time(m=1, s=55, ms=455),
                        text=r"{\i1}Parem!{\i0}",
                        vtt_cue_about={"setting": {"line": "85%", "align": "middle"}}))
    ref.append(SSAEvent(start=make_time(m=1, s=58, ms=155), end=make_time(m=1, s=59, ms=555),
                        text="E, parem!",
                        vtt_cue_about={"setting": {"line": "85%", "align": "middle"}}))
    ref.append(SSAEvent(start=make_time(m=1, s=59, ms=100), end=make_time(m=1, s=59, ms=342),
                        text=""))
    ref.append(SSAEvent(start=make_time(m=2, s=0, ms=100), end=make_time(m=2, s=7, ms=342),
                        text=r'{\N"type": "WikipediaPage",\N"url": "https://en.wikipedia.org/wiki/Samurai_Pizza_Cats"\N}'))
    ref.append(SSAEvent(start=make_time(m=2, s=0, ms=110), end=make_time(m=2, s=0, ms=120),
                        text="NOTE I might add a line to indicate work that still has to be done.",
                        type="Comment",
                        vtt_cue_about={'identifier': 'isnrs'}))

    subs = SSAFile.from_string(text)
    for e, x  in zip(subs, ref):
        print(e.start, e.end, e.text, e.style, e.type, e.vtt_cue_about)
        print(x.start, x.end, x.text, x.style, x.type, x.vtt_cue_about)
    assert subs.equals(ref)

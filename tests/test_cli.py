from typing import Any

import pysubs2
import tempfile
import subprocess
import os.path as op
from io import StringIO

TEST_SRT_FILE = """\
1
00:00:00,000 --> 00:01:00,000
An example subtitle.

2
00:01:00,000 --> 00:02:00,000
Subtitle number
two.

"""

TEST_SRT_FILE_WIN1250 = """\
1
00:00:00,000 --> 00:01:00,000
An example subtitle.
Příliš žluťoučký kůň úpěl ďábelské ódy

"""

TEST_MICRODVD_FILE = """\
{1}{1}1000.0
{0}{60000}An example subtitle.
{60000}{120000}Subtitle number|two.
"""


def test_srt_to_microdvd() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "microdvd", "--fps", "1000", inpath])

        outpath = op.join(dirpath, "test.sub")
        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_MICRODVD_FILE


def test_srt_to_microdvd_subprocess_pipe() -> None:
    cmd = ["python", "-m", "pysubs2", "--to", "microdvd", "--fps", "1000"]
    output = subprocess.check_output(cmd, input=TEST_SRT_FILE, text=True)
    assert output.strip() == TEST_MICRODVD_FILE.strip()


def test_srt_to_microdvd_multiple_files() -> None:
    N = 3
    with tempfile.TemporaryDirectory() as dirpath:
        inpaths = [op.join(dirpath, f"test-{i}.srt") for i in range(N)]
        for inpath in inpaths:
            with open(inpath, "w", encoding="utf-8") as fp:
                fp.write(TEST_SRT_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "microdvd", "--fps", "1000"] + inpaths)

        outpaths = [p.replace(".srt", ".sub") for p in inpaths]
        for outpath in outpaths:
            with open(outpath, encoding="utf-8") as fp:
                out = fp.read()
                assert out == TEST_MICRODVD_FILE


def test_microdvd_to_srt() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = op.join(dirpath, "test.sub")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_MICRODVD_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", inpath])

        outpath = op.join(dirpath, "test.srt")
        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_SRT_FILE


TEST_SRT_FILE_SHIFTED = """\
1
01:00:01,500 --> 01:01:01,500
An example subtitle.

2
01:01:01,500 --> 01:02:01,500
Subtitle number
two.

"""


def test_srt_shift() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = outpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--shift", "1h1.5s", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_SRT_FILE_SHIFTED


def test_srt_shift_back() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = outpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE_SHIFTED)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--shift-back", "1h1.5s", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_SRT_FILE


def test_srt_shift_to_output_dir() -> None:
    with tempfile.TemporaryDirectory() as indirpath:
        inpath = op.join(indirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        with tempfile.TemporaryDirectory() as outdirpath:
            outdirpath2 = op.join(outdirpath, "subdir-that-must-be-created")
            outpath = op.join(outdirpath2, "test.srt")

            cli = pysubs2.cli.Pysubs2CLI()
            cli(["--shift", "1h1.5s", "-o", outdirpath2, inpath])

            with open(outpath, encoding="utf-8") as fp:
                out = fp.read()
                assert out == TEST_SRT_FILE_SHIFTED

            with open(inpath, encoding="utf-8") as fp:
                out = fp.read()
                assert out == TEST_SRT_FILE


TEST_SUBSTATION_WITH_KARAOKE = r"""
[Script Info]
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Volkhov,78,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,0,0,0,0,95,100,0,0,1,3.5,0,2,225,225,50,1
Style: OP-R,Clearface SSi,70,&H00FFFFFF,&HFFA6A6A6,&H004E4AFB,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,40,40,40,1
Style: OP-E,Clearface SSi,55,&H00FFFFFF,&HFFA6A6A6,&H00464646,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,40,40,115,1
Style: ED-R,IM FELL English PRO,78,&H57EAFDFE,&H00B6B6B6,&H00182739,&H8CFFFFFF,0,0,0,0,100,100,0,0,1,5.9,0.1,8,10,10,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 10,0:00:07.24,0:00:10.03,OP-E,,0,0,0,,{\an5\pos(655.758,142.500)\1c&H4E4AFB&\3c&H4E4AFB&\blur2.4\bord2.5\fad(300,300)}I
Dialogue: 11,0:00:07.24,0:00:10.03,OP-E,,0,0,0,,{\an5\pos(655.758,142.500)\bord0\blur0.4\fad(300,300)}I
Dialogue: 10,0:00:07.28,0:00:10.07,OP-E,,0,0,0,,{\an5\pos(691.016,142.500)\1c&H4E4AFB&\3c&H4E4AFB&\blur2.4\bord2.5\fad(300,300)}w
Dialogue: 11,0:00:07.28,0:00:10.07,OP-E,,0,0,0,,{\an5\pos(691.016,142.500)\bord0\blur0.4\fad(300,300)}w
Dialogue: 3,0:23:38.12,0:23:38.16,ED-R,,0,0,0,,{\an7\pos(1113.473,73.684)\bord0\blur0.5\1c&H000000&\p4}m 0 0 l 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 m 0 0 l 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 m 0 0 l 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 m 0 0 l 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Dialogue: 10,0:24:06.45,0:24:09.95,Default,Next time,0,0,0,,Next episode: "Warrior."
Dialogue: 5,0:24:06.45,0:24:09.95,Default,Next time,0,0,0,,{\be1}Next episode: "Warrior."{this duplicate line should be deleted}
"""

TEST_SUBSTATION_WITH_KARAOKE_SRT_CLEAN_OUTPUT = """
1
00:24:06,450 --> 00:24:09,950
Next episode: "Warrior."
"""

TEST_SUBSTATION_WITH_ITALICS = r"""
[Script Info]
; Script generated by Aegisub 3.2.2
; http://www.aegisub.org/
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[Aegisub Project Garbage]
Last Style Storage: Default

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: Default - italic,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Default - italic,,0,0,0,,Italic from style
Dialogue: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,Italic from {\i1}override tag{\i0}
"""

TEST_SUBSTATION_WITH_ITALICS_SRT_CLEAN_OUTPUT = """
1
00:00:00,000 --> 00:00:05,000
Italic from style

2
00:00:05,000 --> 00:00:07,000
Italic from override tag
"""

TEST_SUBSTATION_WITH_ITALICS_SRT_OUTPUT = """
1
00:00:00,000 --> 00:00:05,000
<i>Italic from style</i>

2
00:00:05,000 --> 00:00:07,000
Italic from <i>override tag</i>
"""

TEST_SRT_KEEP_SSA_TAGS = """
1
00:00:00,000 --> 00:01:00,000
{\\an7}An example subtitle.

2
00:01:00,000 --> 00:02:00,000
Subtitle {\\b1}number{\\b0}
two.
"""

TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML = """
1
00:00:00,000 --> 00:01:00,000
{\\an7}An example subtitle.

2
00:01:00,000 --> 00:02:00,000
Subtitle <i>number</i>
two.
"""

TEST_SRT_KEEP_UNKNOWN_HTML_TAGS = """
1
00:00:00,000 --> 00:00:05,000
<i>Italic from style</i>

2
00:00:05,000 --> 00:00:07,000
Some unsupported <blink>tag</blink>
"""


def test_srt_clean() -> None:
    # see issue #37
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = op.join(dirpath, "test.ass")
        outpath = op.join(dirpath, "test.srt")

        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SUBSTATION_WITH_KARAOKE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--clean", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SUBSTATION_WITH_KARAOKE_SRT_CLEAN_OUTPUT.strip()


def test_srt_clean_styling() -> None:
    # see issue #39
    with tempfile.TemporaryDirectory() as dirpath:
        inpath = op.join(dirpath, "test.ass")
        outpath = op.join(dirpath, "test.srt")

        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SUBSTATION_WITH_ITALICS)

        # test standard
        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SUBSTATION_WITH_ITALICS_SRT_OUTPUT.strip()

        # test clean
        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--clean", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SUBSTATION_WITH_ITALICS_SRT_CLEAN_OUTPUT.strip()


def test_srt_keep_ssa_tags() -> None:
    # see issue #48
    with tempfile.TemporaryDirectory() as dirpath:
        path = op.join(dirpath, "test.srt")

        # test standard
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_SSA_TAGS)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() != TEST_SRT_KEEP_SSA_TAGS.strip()

        # test keep tags
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_SSA_TAGS)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--srt-keep-ssa-tags", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SRT_KEEP_SSA_TAGS.strip()


def test_srt_keep_ssa_tags_mixed_with_html() -> None:
    # see issue #48
    with tempfile.TemporaryDirectory() as dirpath:
        path = op.join(dirpath, "test.srt")

        # test standard - does not pass
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() != TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML.strip()

        # test juts keep SSA tags - does not pass
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--srt-keep-ssa-tags", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() != TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML.strip()

        # test keep SSA tags and keep HTML tags - should pass
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--srt-keep-ssa-tags", "--srt-keep-html-tags", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SRT_KEEP_SSA_TAGS_MIXED_WITH_HTML.strip()


def test_srt_keep_unknown_html_tags() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        path = op.join(dirpath, "test.srt")

        # test standard
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_UNKNOWN_HTML_TAGS)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() != TEST_SRT_KEEP_UNKNOWN_HTML_TAGS.strip()

        # test keep tags
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_KEEP_UNKNOWN_HTML_TAGS)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--srt-keep-unknown-html-tags", path])

        with open(path, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SRT_KEEP_UNKNOWN_HTML_TAGS.strip()


def test_print_help_on_empty_tty_input(capsys: Any, monkeypatch: Any) -> None:
    monkeypatch.setattr("sys.stdin", StringIO())
    monkeypatch.setattr("sys.stdin.isatty", (lambda: True))

    cli = pysubs2.cli.Pysubs2CLI()
    cli([])

    captured = capsys.readouterr()
    assert captured.out.startswith("usage: pysubs2")


def test_empty_notty_input_doesnt_print_help(capsys: Any, monkeypatch: Any) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = op.join(temp_dir, "test.srt")
        with open(path, "w+") as in_fp:
            cmd = ["python", "-m", "pysubs2"]
            p = subprocess.run(cmd, stdin=in_fp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            assert p.returncode == 1
            assert not p.stdout.startswith("usage: pysubs2")
            assert "FormatAutodetectionError" in p.stderr


def test_win1250_passthrough_with_surrogateescape() -> None:
    input_bytes_win1250 = TEST_SRT_FILE_WIN1250.encode("windows-1250")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = op.join(temp_dir, "input.srt")
        output_dir = op.join(temp_dir, "output")
        output_path = op.join(output_dir, "input.srt")
        with open(input_path, "wb") as fp:
            fp.write(input_bytes_win1250)

        cmd = ["python", "-m", "pysubs2", "-o", output_dir, input_path]
        subprocess.check_call(cmd)

        with open(output_path, "rb") as fp:
            output_bytes = fp.read()

        assert input_bytes_win1250 == output_bytes

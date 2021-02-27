from __future__ import unicode_literals

import pysubs2
import tempfile
import shutil
import os.path as op
from contextlib import contextmanager
from io import open

@contextmanager
def temp_dir():
    """tempfile.TemporaryDirectory alike (for Python 2.7)"""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


TEST_SRT_FILE = """\
1
00:00:00,000 --> 00:01:00,000
An example subtitle.

2
00:01:00,000 --> 00:02:00,000
Subtitle number
two.

"""

TEST_MICRODVD_FILE = """\
{0}{0}1000.0
{0}{60000}An example subtitle.
{60000}{120000}Subtitle number|two.
"""

def test_srt_to_microdvd():
    with temp_dir() as dirpath:
        inpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "microdvd", "--fps", "1000", inpath])

        outpath = op.join(dirpath, "test.sub")
        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_MICRODVD_FILE

def test_srt_to_microdvd_multiple_files():
    N = 3
    with temp_dir() as dirpath:
        inpaths = [op.join(dirpath, "test-%d.srt" % i) for i in range(N)]
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

def test_microdvd_to_srt():
    with temp_dir() as dirpath:
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

def test_srt_shift():
    with temp_dir() as dirpath:
        inpath = outpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--shift", "1h1.5s", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_SRT_FILE_SHIFTED

def test_srt_shift_back():
    with temp_dir() as dirpath:
        inpath = outpath = op.join(dirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE_SHIFTED)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--shift-back", "1h1.5s", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out == TEST_SRT_FILE

def test_srt_shift_to_output_dir():
    with temp_dir() as indirpath:
        inpath = op.join(indirpath, "test.srt")
        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SRT_FILE)

        with temp_dir() as outdirpath:
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

def test_srt_clean():
    # see issue #37
    with temp_dir() as dirpath:
        inpath = op.join(dirpath, "test.ass")
        outpath = op.join(dirpath, "test.srt")

        with open(inpath, "w", encoding="utf-8") as fp:
            fp.write(TEST_SUBSTATION_WITH_KARAOKE)

        cli = pysubs2.cli.Pysubs2CLI()
        cli(["--to", "srt", "--clean", inpath])

        with open(outpath, encoding="utf-8") as fp:
            out = fp.read()
            assert out.strip() == TEST_SUBSTATION_WITH_KARAOKE_SRT_CLEAN_OUTPUT.strip()

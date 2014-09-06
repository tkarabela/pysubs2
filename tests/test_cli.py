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

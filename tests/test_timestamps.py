"""
test related to Timestamps class

"""

import json
import pytest
from pysubs2 import SSAFile, Timestamps, TimeType
import os.path as op

TIMESTAMPS_PATH = op.join(op.dirname(__file__), "data/timestamps/timestamps.txt")
MS_TO_FRAMES_FPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/timestamps/ms_to_frames_with_fps.ass"
)
MS_TO_FRAMES_TIMESTAMPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/timestamps/ms_to_frames_with_timestamps.ass"
)
FRAMES_TO_MS_FPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/timestamps/frames_to_ms_with_fps.ass"
)
FRAMES_TO_MS_TIMESTAMPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/timestamps/frames_to_ms_with_timestamps.ass"
)
TEST_VIDEO_23976_MKV_PATH = op.join(
    op.dirname(__file__), "data/timestamps/test_video_23.976/test_video.mkv"
)
TEST_VIDEO_23976_SRT_PATH = op.join(
    op.dirname(__file__), "data/timestamps/test_video_23.976/test_video.srt"
)
TEST_VIDEO_23976_TIMESTAMPS_PATH = op.join(
    op.dirname(__file__), "data/timestamps/test_video_23.976/ts-track0.txt"
)


def test_fps_ms_to_frames():
    subs_aegisub = SSAFile.load(MS_TO_FRAMES_FPS_SUBS_PYSUBS_PATH)
    timestamps = Timestamps.from_fps(23.976)

    for line in subs_aegisub:
        try:
            ms = int(line.style)
        except ValueError:
            continue

        time = json.loads(line.text)
        assert time["start_time"] == timestamps.ms_to_frames(ms, TimeType.START)
        assert time["end_time"] == timestamps.ms_to_frames(ms, TimeType.END)


def test_timestamps_ms_to_frames():
    subs_aegisub = SSAFile.load(MS_TO_FRAMES_TIMESTAMPS_SUBS_PYSUBS_PATH)
    timestamps = Timestamps.from_timestamps_file(TIMESTAMPS_PATH)

    for line in subs_aegisub:
        try:
            ms = int(line.style)
        except ValueError:
            continue

        time = json.loads(line.text)
        assert time["start_time"] == timestamps.ms_to_frames(ms, TimeType.START)
        assert time["end_time"] == timestamps.ms_to_frames(ms, TimeType.END)


def test_fps_frames_to_ms():
    subs_aegisub = SSAFile.load(FRAMES_TO_MS_FPS_SUBS_PYSUBS_PATH)
    timestamps = Timestamps.from_fps(23.976)

    for line in subs_aegisub:
        try:
            frame = int(line.style)
        except ValueError:
            continue

        time = json.loads(line.text)
        assert time["start_time"] == timestamps.frames_to_ms(frame, TimeType.START)
        assert time["end_time"] == timestamps.frames_to_ms(frame, TimeType.END)


def test_timestamps_frames_to_ms():
    subs_aegisub = SSAFile.load(FRAMES_TO_MS_TIMESTAMPS_SUBS_PYSUBS_PATH)
    timestamps = Timestamps.from_timestamps_file(TIMESTAMPS_PATH)

    for line in subs_aegisub:
        try:
            frame = int(line.style)
        except ValueError:
            continue

        time = json.loads(line.text)
        assert time["start_time"] == timestamps.frames_to_ms(frame, TimeType.START)
        assert time["end_time"] == timestamps.frames_to_ms(frame, TimeType.END)


def test_timestamps_constructors():
    """This test requires ffprobe(1) to be available"""
    ts_file = Timestamps.from_timestamps_file(TEST_VIDEO_23976_TIMESTAMPS_PATH)
    ts_video = Timestamps.from_video_file(TEST_VIDEO_23976_MKV_PATH)
    ts_fps = Timestamps.from_fps(23.976)

    for i in range(500):
        assert ts_fps.frames_to_ms(i, TimeType.EXACT) == ts_video.frames_to_ms(i, TimeType.EXACT)
        assert ts_fps.frames_to_ms(i, TimeType.EXACT) == ts_file.frames_to_ms(i, TimeType.EXACT)


def test_frames_to_ms():
    timestamps = Timestamps([0, 1000, 1500, 2000, 2001, 2002, 2003])

    assert 0 == timestamps.frames_to_ms(0, TimeType.EXACT)
    assert 1000 == timestamps.frames_to_ms(1, TimeType.EXACT)
    assert 1500 == timestamps.frames_to_ms(2, TimeType.EXACT)
    assert 2000 == timestamps.frames_to_ms(3, TimeType.EXACT)
    assert 2001 == timestamps.frames_to_ms(4, TimeType.EXACT)
    assert 2002 == timestamps.frames_to_ms(5, TimeType.EXACT)
    assert 2003 == timestamps.frames_to_ms(6, TimeType.EXACT)
    with pytest.raises(ValueError) as exc_info:
        timestamps.frames_to_ms(-1, TimeType.EXACT)
    assert str(exc_info.value) == "You cannot specify a frame under 0."

    assert 0 == timestamps.frames_to_ms(0, TimeType.START)
    assert 0 < timestamps.frames_to_ms(1, TimeType.START) <= 1000
    assert 1000 < timestamps.frames_to_ms(2, TimeType.START) <= 1500
    assert 1500 < timestamps.frames_to_ms(3, TimeType.START) <= 2000
    assert 2000 < timestamps.frames_to_ms(4, TimeType.START) <= 2001
    assert 2001 < timestamps.frames_to_ms(5, TimeType.START) <= 2002
    assert 2002 < timestamps.frames_to_ms(6, TimeType.START) <= 2003
    with pytest.raises(ValueError) as exc_info:
        timestamps.frames_to_ms(-1, TimeType.END)
    assert str(exc_info.value) == "You cannot specify a frame under 0."

    assert 0 < timestamps.frames_to_ms(0, TimeType.END) <= 1000
    assert 1000 < timestamps.frames_to_ms(1, TimeType.END) <= 1500
    assert 1500 < timestamps.frames_to_ms(2, TimeType.END) <= 2000
    assert 2000 < timestamps.frames_to_ms(3, TimeType.END) <= 2001
    assert 2001 < timestamps.frames_to_ms(4, TimeType.END) <= 2002
    assert 2002 < timestamps.frames_to_ms(5, TimeType.END) <= 2003
    assert 2003 < timestamps.frames_to_ms(6, TimeType.END)
    with pytest.raises(ValueError) as exc_info:
        timestamps.frames_to_ms(-1, TimeType.END)
    assert str(exc_info.value) == "You cannot specify a frame under 0."


def test_ms_to_frames():
    timestamps = Timestamps([0, 1000, 1500, 2000, 2001, 2002, 2003])

    assert 0 == timestamps.ms_to_frames(0, TimeType.EXACT)
    assert 0 == timestamps.ms_to_frames(999, TimeType.EXACT)
    assert 1 == timestamps.ms_to_frames(1000, TimeType.EXACT)
    assert 1 == timestamps.ms_to_frames(1499, TimeType.EXACT)
    assert 2 == timestamps.ms_to_frames(1500, TimeType.EXACT)
    assert 2 == timestamps.ms_to_frames(1999, TimeType.EXACT)
    assert 3 == timestamps.ms_to_frames(2000, TimeType.EXACT)
    assert 4 == timestamps.ms_to_frames(2001, TimeType.EXACT)
    assert 5 == timestamps.ms_to_frames(2002, TimeType.EXACT)
    assert 6 == timestamps.ms_to_frames(2003, TimeType.EXACT)
    assert 6 == timestamps.ms_to_frames(2004, TimeType.EXACT)
    with pytest.raises(ValueError) as exc_info:
        timestamps.ms_to_frames(-1, TimeType.EXACT)
    assert str(exc_info.value) == "You cannot specify an time under 0."

    assert 0 == timestamps.ms_to_frames(0, TimeType.START)
    assert 1 == timestamps.ms_to_frames(1, TimeType.START)
    assert 1 == timestamps.ms_to_frames(1000, TimeType.START)
    assert 2 == timestamps.ms_to_frames(1001, TimeType.START)
    assert 2 == timestamps.ms_to_frames(1500, TimeType.START)
    assert 3 == timestamps.ms_to_frames(1501, TimeType.START)
    assert 3 == timestamps.ms_to_frames(2000, TimeType.START)
    assert 4 == timestamps.ms_to_frames(2001, TimeType.START)
    assert 5 == timestamps.ms_to_frames(2002, TimeType.START)
    assert 6 == timestamps.ms_to_frames(2003, TimeType.START)
    assert 7 == timestamps.ms_to_frames(2004, TimeType.START)
    with pytest.raises(ValueError) as exc_info:
        timestamps.ms_to_frames(-1, TimeType.START)
    assert str(exc_info.value) == "You cannot specify an time under 0."

    assert -1 == timestamps.ms_to_frames(0, TimeType.END)
    assert 0 == timestamps.ms_to_frames(1, TimeType.END)
    assert 1 == timestamps.ms_to_frames(1500, TimeType.END)
    assert 2 == timestamps.ms_to_frames(1501, TimeType.END)
    assert 2 == timestamps.ms_to_frames(2000, TimeType.END)
    assert 3 == timestamps.ms_to_frames(2001, TimeType.END)
    with pytest.raises(ValueError) as exc_info:
        timestamps.ms_to_frames(-1, TimeType.END)
    assert str(exc_info.value) == "You cannot specify an time under 0."

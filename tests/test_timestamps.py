"""
test of SubStation [Fonts] handling

"""

import json
from pysubs2 import SSAFile, Timestamps, TimeType
import os.path as op

TIMESTAMPS_PATH = op.join(op.dirname(__file__), "data/timestamps.txt")
MS_TO_FRAMES_FPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/ms_to_frames_with_fps.ass"
)
MS_TO_FRAMES_TIMESTAMPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/ms_to_frames_with_timestamps.ass"
)
FRAMES_TO_MS_FPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/frames_to_ms_with_fps.ass"
)
FRAMES_TO_MS_TIMESTAMPS_SUBS_PYSUBS_PATH = op.join(
    op.dirname(__file__), "data/frames_to_ms_with_timestamps.ass"
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

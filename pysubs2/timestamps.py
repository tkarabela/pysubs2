import bisect
import json
import math
import os
import shutil
import subprocess
import sys
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from numbers import Number
from typing import Dict, Type, Union, List


class TimeType(Enum):

    START = "START"
    EXACT = "EXACT"
    END = "END"


class Timestamps:
    """Timestamps object contains informations about the timestamps of an video.

    Parameters:
        timestamps (List[int]): A list of [timestamps](https://en.wikipedia.org/wiki/Timestamp) in milliseconds encoded as integers.
                                It represent each frame [presentation timestamp (PTS)](https://en.wikipedia.org/wiki/Presentation_timestamp)
        set_from_timestamps (bool, optional): If True, then it will does some calculation related on the timestamps. If false, this means the object will approximate frame timestamps.
        normalize (bool, optional): If True, it will shift the timestamps to make them start from 0. If false, the option does nothing.
    """

    timestamps: List[int]
    denominator: int = 1000000000
    numerator: int
    last: int = 0

    def __init__(
        self,
        timestamps: List[int],
        set_from_timestamps: bool = True,
        normalize: bool = True,
    ):

        self.timestamps = timestamps

        if normalize:
            self.timestamps = Timestamps.normalize(self.timestamps)

        if set_from_timestamps:
            Timestamps.validate(self.timestamps)

            self.numerator = int(
                (len(self.timestamps) - 1)
                * self.denominator
                * 1000
                / self.timestamps[-1]
            )
            self.last = (len(self.timestamps) - 1) * self.denominator * 1000

    @classmethod
    def from_fps(
        cls: Type["Timestamps"], fps: Number
    ) -> "Timestamps":
        """Create timestamps based on the `fps` provided.

        Inspired by: https://github.com/Aegisub/Aegisub/blob/6f546951b4f004da16ce19ba638bf3eedefb9f31/libaegisub/common/vfr.cpp#L134-L141

        Args:
            fps (positive int, float or Fraction): Frames per second.
        Returns:
            An Timestamps instance.
        """
        if not 0 < fps <= 1000:
            raise ValueError(
                "Parameter 'fps' must be between 0 and 1000 (0 not included)."
            )

        timestamps = [0]
        cls.numerator = int(fps * cls.denominator)
        return cls(timestamps, False, False)

    @classmethod
    def from_timestamps_file(
        cls: Type["Timestamps"], path_timestamps: str, normalize: bool = True
    ) -> "Timestamps":
        """Parse timestamps from a [timestamp file format v2](https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.external_timestamp_files) and return them.
        To extract the timestamps file, you can use [gMKVExtractGUI](https://sourceforge.net/projects/gmkvextractgui/) for .mkv file.

        Args:
            path_timestamps (str): Path for the timestamps file (either relative to your .py file or absolute).
            normalize (bool): If True, it will shift the timestamps to make them start from 0. If false, the option does nothing.
        Returns:
            An Timestamps instance.
        """
        # Getting timestamps absolute path and checking for its existance
        if not os.path.isabs(path_timestamps):
            dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
            path_timestamps = os.path.join(dirname, path_timestamps)
        if not os.path.isfile(path_timestamps):
            raise FileNotFoundError(
                f'Invalid path for the timestamps file: "{path_timestamps}"'
            )

        # Parsing timestamps
        timestamps = []
        with open(path_timestamps, "r") as f:
            format_version = f.readline().strip().replace("timecode", "timestamp")
            tf = "# timestamp format"

            if format_version in [f"{tf} v1", f"{tf} v3", f"{tf} v4"]:
                raise NotImplementedError(
                    f'The timestamps file "{path_timestamps}" is in a format not currently supported by PyonFX.'
                )

            if format_version != f"{tf} v2":
                raise ValueError(
                    f'The timestamps file "{path_timestamps}" is not properly formatted.'
                )

            while line := f.readline().strip():
                if line.startswith("#") or not line:
                    continue
                try:
                    timestamps.append(int(line))
                except ValueError:
                    raise ValueError(
                        f'The timestamps file "{path_timestamps}" is not properly formatted.'
                    )

        return cls(timestamps, normalize=normalize)

    @classmethod
    def from_video_file(
        cls: Type["Timestamps"], video_path: str, index: int = 0, normalize: bool = True
    ) -> "Timestamps":
        """Create timestamps based on the `video_path` provided.

        Parameters:
            video (str): Video path.
            index (int): Stream index of the video.
        Returns:
            An Timestamps instance.
        """

        def get_pts(packets) -> List[int]:
            pts: List[int] = []

            for packet in packets:
                pts.append(int(Decimal(packet["pts_time"]) * 1000))

            pts.sort()
            return pts

        # Verify if ffprobe is installed
        if shutil.which("ffprobe") is None:
            raise Exception("ffprobe is not in the environment variable.")

        # Getting video absolute path and checking for its existance
        if not os.path.isabs(video_path):
            dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
            video_path = os.path.join(dirname, video_path)
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f'Invalid path for the video file: "{video_path}"')

        cmd = f'ffprobe -select_streams {index} -show_entries packet=pts_time:stream=codec_type "{video_path}" -print_format json'
        ffprobeOutput = subprocess.run(cmd, capture_output=True, text=True)
        ffprobeOutput = json.loads(ffprobeOutput.stdout)

        if len(ffprobeOutput) == 0:
            raise Exception(
                f"The file {video_path} is not a video file or the file does not exist."
            )

        if len(ffprobeOutput["streams"]) == 0:
            raise ValueError(f"The index {index} is not in the file {video_path}.")

        if ffprobeOutput["streams"][0]["codec_type"] != "video":
            raise ValueError(
                f'The index {index} is not a video stream. It is an {ffprobeOutput["streams"][0]["codec_type"]} stream.'
            )

        timestamps = get_pts(ffprobeOutput["packets"])
        return cls(timestamps, normalize=normalize)

    @staticmethod
    def validate(timestamps: List[int]) -> None:
        """Verify that the provided timestamps are valid. Raising ValueError in case they are not.

        Inspired by: https://github.com/Aegisub/Aegisub/blob/6f546951b4f004da16ce19ba638bf3eedefb9f31/libaegisub/common/vfr.cpp#L39-L46

        Args:
            timestamps (list of int): A list of [timestamps](https://en.wikipedia.org/wiki/Timestamp) encoded as integers.
        """
        if len(timestamps) <= 1:
            raise ValueError("There must be at least 2 timestamps.")

        if any(timestamps[i] > timestamps[i + 1] for i in range(len(timestamps) - 1)):
            raise ValueError("Timestamps must be in non-decreasing order.")

        if timestamps.count(timestamps[0]) == len(timestamps):
            raise ValueError("Timestamps must not be all identical.")

    @staticmethod
    def normalize(timestamps: List[int]) -> List[int]:
        """Shift the timestamps to make them start from 0. This way, frame 0 will start at time 0.

        Inspired by: https://github.com/Aegisub/Aegisub/blob/6f546951b4f004da16ce19ba638bf3eedefb9f31/libaegisub/common/vfr.cpp#L50-L53

        Args:
            timestamps (List[int]): A list of [timestamps](https://en.wikipedia.org/wiki/Timestamp) encoded as integers.
        Returns:
            The timestamps normalized.
        """
        if timestamps[0]:
            return list(map(lambda t: t - timestamps[0], timestamps))
        return timestamps


    def ms_to_frames(
        self, ms: int, time_type: TimeType = TimeType.EXACT, approximate: bool = True
    ) -> int:
        """Converts milliseconds to frames.

        Inspired by: https://github.com/arch1t3cht/Aegisub/blob/245cc68afabefbc9290bd5a13ec327a59fe23b6d/libaegisub/common/vfr.cpp#L205-L231

        Parameters:
            ms (int): Milliseconds.
            time_type (TimeType, optional): The type of the provided time (start/end).
            approximate (bool, optional): If True and if the ms is under 0 or over the video length, it will approximate the frame.
        Returns:
            The output represents ``ms`` converted into ``frames``.
        """

        if not approximate:
            if ms < 0:
                raise ValueError("You cannot specify an time under 0.")
            elif ms > self.timestamps[-1]:
                raise ValueError("You cannot specify an time over the video lenght.")

        if time_type == TimeType.START:
            return self.ms_to_frames(ms - 1) + 1
        elif time_type == TimeType.END:
            return self.ms_to_frames(ms - 1)

        if ms < 0:
            return int(int(ms * self.numerator / self.denominator - 999) / 1000)
        elif ms > self.timestamps[-1]:
            return (
                int(
                    int(
                        (
                            ms * self.numerator
                            - int(self.numerator / 2)
                            - self.last
                            + self.numerator
                            - 1
                        )
                        / self.denominator
                    )
                    / 1000
                )
                + len(self.timestamps)
                - 1
            )

        return bisect.bisect_right(self.timestamps, ms) - 1

    def frames_to_ms(
        self,
        frame: int,
        time_type: TimeType = TimeType.EXACT,
        approximate: bool = True,
    ) -> int:
        """Converts frames to milliseconds.

        Inspired by: https://github.com/Aegisub/Aegisub/blob/6f546951b4f004da16ce19ba638bf3eedefb9f31/libaegisub/common/vfr.cpp#L233-L256

        Parameters:
            frame (int): Frame.
            format (str): Subtitle format. Ex: "srt", "ass", "ssa", etc...
            time_type (TimeType, optional): The type of the provided time (start/end).
            approximate (bool, optional): If True and if the frame is under 0 or over the video length, it will approximate the ms.
        Returns:
            The output represents ``frames`` converted into ``ms``.
        """

        if not approximate:
            if frame < 0:
                raise ValueError("You cannot specify a frame under 0.")
            elif frame > len(self.timestamps) - 1:
                raise ValueError(
                    "You cannot specify an image above what the video length."
                )

        if time_type == TimeType.START:
            # Previous image excluded
            prev_ms = self.frames_to_ms(frame - 1) + 1
            # Current image inclued
            curr_ms = self.frames_to_ms(frame)

            return prev_ms + int((curr_ms - prev_ms) / 2)

        elif time_type == TimeType.END:
            # Current image excluded
            curr_ms = self.frames_to_ms(frame) + 1
            # Next image inclued
            next_ms = self.frames_to_ms(frame + 1)

            return curr_ms + int((next_ms - curr_ms) / 2)

        if frame < 0:
            return int(frame * self.denominator * 1000 / self.numerator)
        elif frame > len(self.timestamps) - 1:
            frames_past_end = frame - len(self.timestamps) + 1
            return int(
                (
                    frames_past_end * 1000 * self.denominator
                    + self.last
                    + int(self.numerator / 2)
                )
                / self.numerator
            )

        return self.timestamps[frame]
from __future__ import print_function, unicode_literals

from .formatbase import FormatBase
from ..time import ms_to_times


def ms_to_timestamp(ms):
    """Convert ms to 'HH:MM:SS,mmm' or raise OverflowError."""
    ms = max(ms, 0) # XXX warn here
    h, m, s, ms = ms_to_times(ms)
    if h >= 100:
        raise OverflowError("SRT timestamp cannot represent >=100 hours.")
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


class SubripFormat(FormatBase):
    @classmethod
    def guess_format(cls, text):
        # XXX fragile, improve, line with 2 timestamps very soon in file
        if "-->" in text:
            return "srt"

    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        # XXX implement this
        raise NotImplementedError("Writing is not supported for this format")

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        visible_lines = [line for line in subs if not line.is_comment]

        for i, line in enumerate(visible_lines, 1):
            start = ms_to_timestamp(line.start)
            end = ms_to_timestamp(line.end)
            text = line.text # XXX convert tags to srt

            print("%d" % i, file=fp) # Python 2.7 compat
            print(start, "-->", end, file=fp)
            print(text, end="\n\n", file=fp)

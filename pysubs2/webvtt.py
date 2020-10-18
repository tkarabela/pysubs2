import re
from .subrip import SubripFormat
from .time import make_time


class WebVTTFormat(SubripFormat):
    TIMESTAMP = re.compile(r"(\d{0,4}:)?(\d{2}):(\d{2})\.(\d{2,3})")

    @staticmethod
    def timestamp_to_ms(groups):
        _h, _m, _s, _ms = groups
        if not _h:
            h = 0
        else:
            h = int(_h.strip(":"))
        m, s, ms = map(int, (_m, _s, _ms))
        return make_time(h=h, m=m, s=s, ms=ms)

    @classmethod
    def guess_format(cls, text):
        if text.lstrip().startswith("WEBVTT"):
            return "vtt"

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        print("WEBVTT\n", file=fp)
        return SubripFormat.to_file(subs=subs, fp=fp, format_=format_, **kwargs)

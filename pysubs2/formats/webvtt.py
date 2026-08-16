# mypy: disable-error-code="override"

import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, TextIO, Unpack, override

from ..ssaevent import SSAEvent
from ..time import make_time
from .subrip import SubripFormat

if TYPE_CHECKING:
    from ..ssafile import SSAFile


class WebVTTFormat(SubripFormat):
    """
    Web Video Text Tracks (WebVTT) subtitle format implementation

    Currently, this shares implementation with :class:`pysubs2.formats.subrip.SubripFormat`.
    """
    TIMESTAMP = re.compile(r"(\d{0,4}:)?(\d{2}):(\d{2})\.(\d{2,3})")

    class ReaderArgs(SubripFormat.ReaderArgs):
        pass

    class WriterArgs(SubripFormat.WriterArgs):
        pass

    @staticmethod
    @override
    def ms_to_timestamp(ms: int) -> str:
        result = SubripFormat.ms_to_timestamp(ms)
        return result.replace(',', '.')

    @staticmethod
    @override
    def timestamp_to_ms(groups: Sequence[str]) -> int:
        _h, _m, _s, _ms = groups
        if not _h:
            h = 0
        else:
            h = int(_h.strip(":"))
        m, s, ms = map(int, (_m, _s, _ms))
        return make_time(h=h, m=m, s=s, ms=ms)

    @classmethod
    @override
    def guess_format(cls, text: str) -> str | None:
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if text.lstrip().startswith("WEBVTT"):
            return "vtt"
        else:
            return None

    @classmethod
    @override
    def from_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[ReaderArgs]) -> None:
        """
        See :meth:`pysubs2.formats.SubripFormat.from_file()`, additional SRT options are supported by VTT as well
        """
        return super().from_file(subs, fp, format_, **kwargs)

    @classmethod
    @override
    def to_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[WriterArgs]) -> None:
        """
        See :meth:`pysubs2.formats.SubripFormat.to_file()`, additional SRT options are supported by VTT as well
        """
        print("WEBVTT\n", file=fp)
        return super().to_file(subs=subs, fp=fp, format_=format_, **kwargs)

    @classmethod
    @override
    def _get_visible_lines(cls, subs: "SSAFile") -> list[SSAEvent]:
        visible_lines = super()._get_visible_lines(subs)
        visible_lines.sort(key=lambda e: e.start)
        return visible_lines

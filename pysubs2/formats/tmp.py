# mypy: disable-error-code="override"

import re
import warnings
from typing import TYPE_CHECKING, NotRequired, TextIO, TypedDict, Unpack, override

from ..ssaevent import SSAEvent
from ..ssastyle import SSAStyle
from ..time import TIMESTAMP_SHORT, make_time, ms_to_times, timestamp_to_ms
from ..warnings import (
    PossibleMissedSubtitleWarning,
    TimestampOverflow,
    TimestampUnderflow,
)
from .base import FormatBase
from .substation import parse_tags

if TYPE_CHECKING:
    from ..ssafile import SSAFile


#: Pattern that matches TMP line
TMP_LINE = re.compile(r"(\d{1,2}:\d{2}:\d{2}):(.+)")

#: Largest timestamp allowed in Tmp, ie. 99:59:59.
MAX_REPRESENTABLE_TIME = make_time(h=99, m=59, s=59)


class TmpFormat(FormatBase):
    """TMP subtitle format implementation"""

    class ReaderArgs(TypedDict):
        pass

    class WriterArgs(TypedDict):
        apply_styles: NotRequired[bool]

    @staticmethod
    def ms_to_timestamp(ms: int) -> str:
        """Convert ms to 'HH:MM:SS'"""
        if ms < 0:
            warnings.warn("Underflow in TMP timestamp, clamping to zero", TimestampUnderflow)
            ms = 0
        elif ms > MAX_REPRESENTABLE_TIME:
            warnings.warn("Overflow in TMP timestamp, clamping to MAX_REPRESENTABLE_TIME", TimestampOverflow)
            ms = MAX_REPRESENTABLE_TIME
        h, m, s, _ = ms_to_times(ms)
        return f"{h:02d}:{m:02d}:{s:02d}"

    @classmethod
    @override
    def guess_format(cls, text: str) -> str | None:
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if "[Script Info]" in text or "[V4+ Styles]" in text:
            # disambiguation vs. SSA/ASS
            return None

        for line in text.splitlines():
            if TMP_LINE.match(line) and len(TMP_LINE.findall(line)) == 1:
                return "tmp"

        return None

    @classmethod
    @override
    def from_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[ReaderArgs]) -> None:
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        events = []

        def prepare_text(text: str) -> str:
            text = text.replace("|", r"\N")  # convert newlines
            text = re.sub(r"< *u *>", r"{\\u1}", text)
            text = re.sub(r"< */? *[a-zA-Z][^>]*>", "", text) # strip other HTML tags
            return text

        for lineno, line in enumerate(fp, 1):
            match = TMP_LINE.match(line)
            if not match:
                if re.search(r"\w", line):
                    warnings.warn(
                        f"Possible missed subtitle at line {lineno}",
                        PossibleMissedSubtitleWarning
                    )
                continue

            start, text = match.groups()
            match2 = TIMESTAMP_SHORT.match(start)
            assert match2 is not None, "TMP_LINE contains TIMESTAMP_SHORT"
            start = timestamp_to_ms(match2.groups())

            # Unfortunately, end timestamp is not given; try to estimate something reasonable:
            # start + 500 ms + 67 ms/character (15 chars per second)
            end_guess = start + 500 + (len(line) * 67)

            event = SSAEvent(start=start, end=end_guess, text=prepare_text(text))
            events.append(event)

        # correct any overlapping subtitles created by end_guess
        for i in range(len(events) - 1):
            events[i].end = min(events[i].end, events[i+1].start)

        subs.events = events

    @classmethod
    @override
    def to_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[WriterArgs]) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.to_file()`

        Italic, underline and strikeout styling is supported.

        Keyword args:
            apply_styles: If False, do not write any styling.

        """
        apply_styles: bool = kwargs.get("apply_styles", True)

        def prepare_text(text: str, style: SSAStyle) -> str:
            body = []
            for fragment, sty in parse_tags(text, style, subs.styles):
                fragment = fragment.replace(r"\h", " ")
                fragment = fragment.replace(r"\n", "\n")
                fragment = fragment.replace(r"\N", "\n")
                if apply_styles:
                    if sty.italic:
                        fragment = f"<i>{fragment}</i>"
                    if sty.underline:
                        fragment = f"<u>{fragment}</u>"
                    if sty.strikeout:
                        fragment = f"<s>{fragment}</s>"
                body.append(fragment)

            return re.sub("\n+", "|", "".join(body).strip())

        for line in subs.get_text_events():
            start = cls.ms_to_timestamp(line.start)
            text = prepare_text(line.text, subs.styles.get(line.style, SSAStyle.DEFAULT_STYLE))

            print(start + ":" + text, end="\n", file=fp)

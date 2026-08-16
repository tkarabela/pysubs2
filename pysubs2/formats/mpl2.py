# mypy: disable-error-code="override"

import re
import warnings
from typing import TYPE_CHECKING, TextIO, TypedDict, Unpack, override

from ..ssaevent import SSAEvent
from ..time import times_to_ms
from ..warnings import PossibleMissedSubtitleWarning
from .base import FormatBase

if TYPE_CHECKING:
    from ..ssafile import SSAFile


# thanks to http://otsaloma.io/gaupol/doc/api/aeidon.files.mpl2_source.html
MPL2_FORMAT = re.compile(r"^\[(-?\d+)\]\[(-?\d+)\](.*)", re.MULTILINE)


class MPL2Format(FormatBase):
    """MPL2 subtitle format implementation"""

    class ReaderArgs(TypedDict):
        pass

    class WriterArgs(TypedDict):
        pass

    @classmethod
    @override
    def guess_format(cls, text: str) -> str | None:
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if MPL2_FORMAT.search(text):
            return "mpl2"
        else:
            return None

    @classmethod
    @override
    def from_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[ReaderArgs]) -> None:
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        def prepare_text(lines: str) -> str:
            out = []
            for s in lines.split("|"):
                s = s.strip()

                if s.startswith("/"):
                    # line beginning with '/' is in italics
                    s = r"{\i1}" + s[1:].strip() + r"{\i0}"

                out.append(s)
            return "\\N".join(out)

        for lineno, line in enumerate(fp, 1):
            if (m := MPL2_FORMAT.search(line)) is not None:
                start, end, text = m.groups()
                e = SSAEvent(
                    start=times_to_ms(s=float(start) / 10),
                    end=times_to_ms(s=float(end) / 10),
                    text=prepare_text(text),
                )
                subs.append(e)
            elif re.search(r"\w", line):
                warnings.warn(
                    f"Possible missed subtitle at line {lineno}",
                    PossibleMissedSubtitleWarning
                )

    @classmethod
    @override
    def to_file(cls, subs: "SSAFile", fp: TextIO, format_: str, **kwargs: Unpack[WriterArgs]) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.to_file()`

        No styling is supported at the moment.

        """
        # TODO handle italics
        for line in subs.get_text_events():
            start = int(line.start // 100)
            end = int(line.end // 100)
            text = line.plaintext.replace("\n", "|")
            print(f"[{start}][{end}] {text}", file=fp)

import re
import warnings
from typing import Sequence, Optional, TextIO, Any

from .base import FormatBase
from ..ssaevent import SSAEvent
from ..ssastyle import SSAStyle
from .substation import parse_tags
from ..time import ms_to_times, make_time, TIMESTAMP, timestamp_to_ms
from ..ssafile import SSAFile


#: Largest timestamp allowed in SubRip, ie. 99:59:59,999.
MAX_REPRESENTABLE_TIME = make_time(h=100) - 1

#: Arrow separator used in SRT/VTT timing lines (``-->`` or the looser ``->``).
TIMESTAMP_ARROW = re.compile(r"-+>")


class SubripFormat(FormatBase):
    """SubRip Text (SRT) subtitle format implementation"""
    TIMESTAMP = TIMESTAMP

    @staticmethod
    def ms_to_timestamp(ms: int) -> str:
        """Convert ms to 'HH:MM:SS,mmm'"""
        if ms < 0:
            ms = 0
        if ms > MAX_REPRESENTABLE_TIME:
            warnings.warn("Overflow in SubRip timestamp, clamping to MAX_REPRESENTABLE_TIME", RuntimeWarning)
            ms = MAX_REPRESENTABLE_TIME
        h, m, s, ms = ms_to_times(ms)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @staticmethod
    def timestamp_to_ms(groups: Sequence[str]) -> int:
        return timestamp_to_ms(groups)

    @classmethod
    def _parse_timestamp_line(cls, line: str) -> Optional[tuple[int, int]]:
        """Return (start_ms, end_ms) if *line* is an SRT/VTT timing line.

        A timing line must have a timestamp, then ``->`` / ``-->``, then another
        timestamp. Dialogue that merely mentions two clock times (for example
        ``Meet at 10:00:00,000 to 11:00:00,000``) is not treated as a cue.
        """
        arrow = TIMESTAMP_ARROW.search(line)
        if arrow is None:
            return None

        left, right = line[:arrow.start()], line[arrow.end():]
        left_stamps = cls.TIMESTAMP.findall(left)
        right_stamps = cls.TIMESTAMP.findall(right)
        if len(left_stamps) != 1 or not right_stamps:
            return None
        if cls.TIMESTAMP.match(left.lstrip()) is None:
            return None

        return cls.timestamp_to_ms(left_stamps[0]), cls.timestamp_to_ms(right_stamps[0])

    @classmethod
    def _is_broken_timestamp_line(cls, line: str) -> bool:
        """True if *line* looks like a timing line but cannot be parsed."""
        if TIMESTAMP_ARROW.search(line) is None:
            return False
        if cls._parse_timestamp_line(line) is not None:
            return False
        return cls.TIMESTAMP.match(line.lstrip()) is not None

    @classmethod
    def guess_format(cls, text: str) -> Optional[str]:
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if "[Script Info]" in text or "[V4+ Styles]" in text:
            # disambiguation vs. SSA/ASS
            return None

        if text.lstrip().startswith("WEBVTT"):
            # disambiguation vs. WebVTT
            return None

        if "http://www.w3.org/ns/ttml" in text:
            # disambiguation vs. TTML
            return None

        for line in text.splitlines():
            if cls._parse_timestamp_line(line) is not None:
                return "srt"

        return None

    @classmethod
    def from_file(cls, subs: "SSAFile", fp: TextIO, format_: str, keep_html_tags: bool = False,
                  keep_unknown_html_tags: bool = False, **kwargs: Any) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.from_file()`

        Supported tags:

          - ``<i>``
          - ``<u>``
          - ``<s>``
          - ``<b>``

        Keyword args:
            keep_html_tags: If True, all HTML tags will be kept as-is instead of being
                converted to SubStation tags (eg. you will get ``<i>example</i>`` instead of ``{\\i1}example{\\i0}``).
                Setting this to True overrides the ``keep_unknown_html_tags`` option.
            keep_unknown_html_tags: If True, supported HTML tags will be converted
                to SubStation tags and any other HTML tags will be kept as-is
                (eg. you would get ``<blink>example {\\i1}text{\\i0}</blink>``).
                If False, these other HTML tags will be stripped from output
                (in the previous example, you would get only ``example {\\i1}text{\\i0}``).
        """
        timestamps: list[tuple[int, int]] = [] # (start, end)
        following_lines: list[list[str]] = [] # contains lists of lines following each timestamp

        for line in fp:
            parsed = cls._parse_timestamp_line(line)
            if parsed is not None:
                timestamps.append(parsed)
                following_lines.append([])
            else:
                if cls._is_broken_timestamp_line(line):
                    warnings.warn(
                        f"Skipping invalid subtitle timestamp line: {line.strip()!r}",
                        RuntimeWarning,
                        stacklevel=2,
                    )
                if timestamps:
                    following_lines[-1].append(line)

        def prepare_text(lines: list[str]) -> str:
            # Handle the "happy" empty subtitle case, which is timestamp line followed by blank line(s)
            # followed by number line and timestamp line of the next subtitle. Fixes issue #11.
            if (len(lines) >= 2
                    and all(re.match(r"\s*$", line) for line in lines[:-1])
                    and re.match(r"\s*\d+\s*$", lines[-1])):
                return ""

            # Handle the general case.
            s = "".join(lines).strip()
            s = re.sub(r"\n+ *\d+ *$", "", s) # strip number of next subtitle
            if not keep_html_tags:
                s = re.sub(r"< *i *>", r"{\\i1}", s)
                s = re.sub(r"< */ *i *>", r"{\\i0}", s)
                s = re.sub(r"< *s *>", r"{\\s1}", s)
                s = re.sub(r"< */ *s *>", r"{\\s0}", s)
                s = re.sub(r"< *u *>", r"{\\u1}", s)
                s = re.sub(r"< */ *u *>", r"{\\u0}", s)
                s = re.sub(r"< *b *>", r"{\\b1}", s)
                s = re.sub(r"< */ *b *>", r"{\\b0}", s)
            if not (keep_html_tags or keep_unknown_html_tags):
                s = re.sub(r"< */? *[a-zA-Z][^>]*>", "", s) # strip other HTML tags
            s = re.sub(r"\n", r"\\N", s) # convert newlines
            return s

        for (start, end), lines in zip(timestamps, following_lines):
            e = SSAEvent(start=start, end=end, text=prepare_text(lines))
            subs.append(e)

    @classmethod
    def to_file(cls, subs: "SSAFile", fp: TextIO, format_: str, apply_styles: bool = True,
                keep_ssa_tags: bool = False, **kwargs: Any) -> None:
        """
        See :meth:`pysubs2.formats.FormatBase.to_file()`

        Italic, underline and strikeout styling is supported.

        Keyword args:
            apply_styles: If False, do not write any styling (ignore line style
                and override tags).
            keep_ssa_tags: If True, instead of trying to convert inline override
                tags to HTML (as supported by SRT), any inline tags will be passed
                to output (eg. ``{\\an7}``, which would be otherwise stripped;
                or ``{\\b1}`` instead of ``<b>``). Whitespace tags ``\\h``, ``\\n``
                and ``\\N`` will always be converted to whitespace regardless of
                this option. In the current implementation, enabling this option
                disables processing of line styles - you will get inline tags but
                if for example line's style is italic you will not get ``{\\i1}``
                at the beginning of the line. (Since this option is mostly useful
                for dealing with non-standard SRT files, ie. both input and output
                is SRT which doesn't use line styles - this shouldn't be much
                of an issue in practice.)
        """
        def prepare_text(text: str, style: SSAStyle) -> str:
            text = text.replace(r"\h", " ")
            text = text.replace(r"\n", "\n")
            text = text.replace(r"\N", "\n")

            body = []
            if keep_ssa_tags:
                body.append(text)
            else:
                for fragment, sty in parse_tags(text, style, subs.styles):
                    if apply_styles:
                        if sty.italic:
                            fragment = f"<i>{fragment}</i>"
                        if sty.underline:
                            fragment = f"<u>{fragment}</u>"
                        if sty.strikeout:
                            fragment = f"<s>{fragment}</s>"
                    body.append(fragment)

            return re.sub("\n+", "\n", "".join(body).strip())

        for lineno, line in enumerate(cls._get_visible_lines(subs), 1):
            start = cls.ms_to_timestamp(line.start)
            end = cls.ms_to_timestamp(line.end)
            text = prepare_text(line.text, subs.styles.get(line.style, SSAStyle.DEFAULT_STYLE))

            print(lineno, file=fp)
            print(start, "-->", end, file=fp)
            print(text, end="\n\n", file=fp)
            lineno += 1

    @classmethod
    def _get_visible_lines(cls, subs: "SSAFile") -> list[SSAEvent]:
        return subs.get_text_events()

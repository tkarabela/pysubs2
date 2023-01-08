from numbers import Number
from typing import Union
import re
from .exceptions import UnknownFPSError
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .formatbase import FormatBase
from .substation import parse_tags
from .timestamps import Timestamps, TimeType

#: Matches a MicroDVD line.
MICRODVD_LINE = re.compile(r" *\{ *(\d+) *\} *\{ *(\d+) *\}(.+)")


class MicroDVDFormat(FormatBase):
    """MicroDVD subtitle format implementation"""
    @classmethod
    def guess_format(cls, text):
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if any(map(MICRODVD_LINE.match, text.splitlines())):
            return "microdvd"

    @classmethod
    def from_file(cls, subs, fp, format_, fps:Union[None,Number,Timestamps] = None, **kwargs):
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        if isinstance(fps, Number):
            timestamps = Timestamps.from_fps(fps)
        elif isinstance(fps, Timestamps):
            timestamps = fps

        for line in fp:
            match = MICRODVD_LINE.match(line)
            if not match:
                continue

            fstart, fend, text = match.groups()
            fstart, fend = map(int, (fstart, fend))

            if fps is None:
                # We don't know the framerate, but it is customary to include
                # it as text of the first subtitle. In that case, we skip
                # this auxiliary subtitle and proceed with reading.
                try:
                    fps = float(text)
                    subs.fps = fps
                    timestamps = Timestamps.from_fps(subs.fps)
                    continue
                except ValueError:
                    raise UnknownFPSError("Framerate was not specified and "
                                          "cannot be read from "
                                          "the MicroDVD file.")

            # I chose the format SRT, but it could be anyone.
            # SRT simply has a precision in milliseconds which can be better.
            start = timestamps.frames_to_ms(fstart, "srt", TimeType.START)
            end = timestamps.frames_to_ms(fend, "srt", TimeType.END)

            def prepare_text(text):
                text = text.replace("|", r"\N")

                def style_replacer(match: re.Match) -> str:
                    tags = [c for c in "biu" if c in match.group(0)]
                    return "{%s}" % "".join(f"\\{c}1" for c in tags)

                text = re.sub(r"\{[Yy]:[^}]+\}", style_replacer, text)
                text = re.sub(r"\{[Ff]:([^}]+)\}", r"{\\fn\1}", text)
                text = re.sub(r"\{[Ss]:([^}]+)\}", r"{\\fs\1}", text)
                text = re.sub(r"\{P:(\d+),(\d+)\}", r"{\\pos(\1,\2)}", text)

                return text.strip()

            ev = SSAEvent(start=start, end=end, text=prepare_text(text))
            subs.append(ev)

    @classmethod
    def to_file(cls, subs, fp, format_, fps:Union[None,Number,Timestamps] = None, write_fps_declaration=True, apply_styles=True, **kwargs):
        """
        See :meth:`pysubs2.formats.FormatBase.to_file()`

        The only supported styling is marking whole lines italic.

        Keyword args:
            write_fps_declaration: If True, create a zero-duration first subtitle which will contain
                the fps.
            apply_styles: If False, do not write any styling.

        """
        if fps is None:
            fps = subs.fps

        if fps is None:
            raise UnknownFPSError("Framerate must be specified when writing MicroDVD.")
        elif isinstance(fps, Number):
            timestamps = Timestamps.from_fps(fps)
        elif isinstance(fps, Timestamps):
            timestamps = fps

        def is_entirely_italic(line: SSAEvent) -> bool:
            style = subs.styles.get(line.style, SSAStyle.DEFAULT_STYLE)
            for fragment, sty in parse_tags(line.text, style, subs.styles):
                fragment = fragment.replace(r"\h", " ")
                fragment = fragment.replace(r"\n", "\n")
                fragment = fragment.replace(r"\N", "\n")
                if not sty.italic and fragment and not fragment.isspace():
                    return False
            return True

        # insert an artificial first line telling the framerate
        if write_fps_declaration:
            subs.insert(0, SSAEvent(start=0, end=0, text=str(fps)))

        for line in subs:
            if line.is_comment or line.is_drawing:
                continue

            text = "|".join(line.plaintext.splitlines())
            if apply_styles and is_entirely_italic(line):
                text = "{Y:i}" + text

            start = timestamps.ms_to_frames(line.start, TimeType.START)
            end = timestamps.ms_to_frames(line.end, TimeType.END)

            # XXX warn on underflow?
            if start < 0: start = 0
            if end < 0: end = 0

            print("{%d}{%d}%s" % (start, end, text), file=fp)

        # remove the artificial framerate-telling line
        if write_fps_declaration:
            subs.pop(0)

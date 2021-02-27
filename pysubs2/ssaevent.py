import re
from typing import Optional, Dict, Any

from .common import IntOrFloat
from .time import ms_to_str, make_time


class SSAEvent:
    """
    A SubStation Event, ie. one subtitle.

    In SubStation, each subtitle consists of multiple "fields" like Start, End and Text.
    These are exposed as attributes (note that they are lowercase; see :attr:`SSAEvent.FIELDS` for a list).
    Additionaly, there are some convenience properties like :attr:`SSAEvent.plaintext` or :attr:`SSAEvent.duration`.

    This class defines an ordering with respect to (start, end) timestamps.

    .. tip :: Use :func:`pysubs2.make_time()` to get times in milliseconds.

    Example::

        >>> ev = SSAEvent(start=make_time(s=1), end=make_time(s=2.5), text="Hello World!")

    """
    OVERRIDE_SEQUENCE = re.compile(r"{[^}]*}")

    #: All fields in SSAEvent.
    FIELDS = frozenset([
        "start", "end", "text", "marked", "layer", "style",
        "name", "marginl", "marginr", "marginv", "effect", "type"
    ])

    def __init__(self,
                 start: int = 0,
                 end: int = 10000,
                 text: str = "",
                 marked: bool = False,
                 layer: int = 0,
                 style: str = "Default",
                 name: str = "",
                 marginl: int = 0,
                 marginr: int = 0,
                 marginv: int = 0,
                 effect: str = "",
                 type: str = "Dialogue"):
        self.start: int = start  #: Subtitle start time (in milliseconds)
        self.end: int = end  #: Subtitle end time (in milliseconds)
        self.text: str = text  #: Text of subtitle (with SubStation override tags)
        self.marked: bool = marked  #: (SSA only)
        self.layer: int = layer  #: Layer number, 0 is the lowest layer (ASS only)
        self.style: str = style  #: Style name
        self.name: str = name  #: Actor name
        self.marginl: int = marginl  #: Left margin
        self.marginr: int = marginr  #: Right margin
        self.marginv: int = marginv  #: Vertical margin
        self.effect: str = effect  #: Line effect
        self.type: str = type  #: Line type (Dialogue/Comment)

    @property
    def duration(self) -> IntOrFloat:
        """
        Subtitle duration in milliseconds (read/write property).

        Writing to this property adjusts :attr:`SSAEvent.end`.
        Setting negative durations raises :exc:`ValueError`.
        """
        return self.end - self.start

    @duration.setter
    def duration(self, ms: int):
        if ms >= 0:
            self.end = self.start + ms
        else:
            raise ValueError("Subtitle duration cannot be negative")

    @property
    def is_comment(self) -> bool:
        """
        When true, the subtitle is a comment, ie. not visible (read/write property).

        Setting this property is equivalent to changing
        :attr:`SSAEvent.type` to ``"Dialogue"`` or ``"Comment"``.
        """
        return self.type == "Comment"

    @is_comment.setter
    def is_comment(self, value: bool):
        if value:
            self.type = "Comment"
        else:
            self.type = "Dialogue"

    @property
    def is_drawing(self) -> bool:
        """Returns True if line is SSA drawing tag (ie. not text)"""
        from .substation import parse_tags
        return any(sty.drawing for _, sty in parse_tags(self.text))

    @property
    def plaintext(self) -> str:
        """
        Subtitle text as multi-line string with no tags (read/write property).

        Writing to this property replaces :attr:`SSAEvent.text` with given plain
        text. Newlines are converted to ``\\N`` tags.
        """
        text = self.text
        text = self.OVERRIDE_SEQUENCE.sub("", text)
        text = text.replace(r"\h", " ")
        text = text.replace(r"\n", "\n")
        text = text.replace(r"\N", "\n")
        return text

    @plaintext.setter
    def plaintext(self, text: str):
        self.text = text.replace("\n", r"\N")

    def shift(self, h: IntOrFloat=0, m: IntOrFloat=0, s: IntOrFloat=0, ms: IntOrFloat=0,
              frames: Optional[int]=None, fps: Optional[float]=None):
        """
        Shift start and end times.

        See :meth:`SSAFile.shift()` for full description.

        """
        delta = make_time(h=h, m=m, s=s, ms=ms, frames=frames, fps=fps)
        self.start += delta
        self.end += delta

    def copy(self) -> "SSAEvent":
        """Return a copy of the SSAEvent."""
        return SSAEvent(**self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return {field: getattr(self, field) for field in self.FIELDS}

    def equals(self, other: "SSAEvent") -> bool:
        """Field-based equality for SSAEvents."""
        if isinstance(other, SSAEvent):
            return self.as_dict() == other.as_dict()
        else:
            raise TypeError("Cannot compare to non-SSAEvent object")

    def __eq__(self, other: "SSAEvent"):
        # XXX document this
        return self.start == other.start and self.end == other.end

    def __ne__(self, other: "SSAEvent"):
        return self.start != other.start or self.end != other.end

    def __lt__(self, other: "SSAEvent"):
        return (self.start, self.end) < (other.start, other.end)

    def __le__(self, other: "SSAEvent"):
        return (self.start, self.end) <= (other.start, other.end)

    def __gt__(self, other: "SSAEvent"):
        return (self.start, self.end) > (other.start, other.end)

    def __ge__(self, other: "SSAEvent"):
        return (self.start, self.end) >= (other.start, other.end)

    def __repr__(self):
        return f"<SSAEvent type={self.type} start={ms_to_str(self.start)} end={ms_to_str(self.end)} text={self.text!r}>"

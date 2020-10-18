from typing import Dict, Any

from .common import Color


class SSAStyle:
    """
    A SubStation Style.

    In SubStation, each subtitle (:class:`SSAEvent`) is associated with a style which defines its font, color, etc.
    Like a subtitle event, a style also consists of "fields"; see :attr:`SSAStyle.FIELDS` for a list
    (note the spelling, which is different from SubStation proper).

    Subtitles and styles are connected via an :class:`SSAFile` they belong to. :attr:`SSAEvent.style` is a string
    which is (or should be) a key in the :attr:`SSAFile.styles` dict. Note that style name is stored separately;
    a given :class:`SSAStyle` instance has no particular name itself.

    This class defines equality (equality of all fields).

    """
    DEFAULT_STYLE: "SSAStyle" = None

    #: All fields in SSAStyle.
    FIELDS = frozenset([
        "fontname", "fontsize", "primarycolor", "secondarycolor",
        "tertiarycolor", "outlinecolor", "backcolor",
        "bold", "italic", "underline", "strikeout",
        "scalex", "scaley", "spacing", "angle", "borderstyle",
        "outline", "shadow", "alignment",
        "marginl", "marginr", "marginv", "alphalevel", "encoding"
    ])

    def __init__(self,
                 fontname: str = "Arial",
                 fontsize: float = 20.0,
                 primarycolor: Color = Color(255, 255, 255, 0),
                 secondarycolor: Color = Color(255, 0, 0, 0),
                 tertiarycolor: Color = Color(0, 0, 0, 0),
                 outlinecolor: Color = Color(0, 0, 0, 0),
                 backcolor: Color = Color(0, 0, 0, 0),
                 bold: bool = False,
                 italic: bool = False,
                 underline: bool = False,
                 strikeout: bool = False,
                 scalex: float = 100.0,
                 scaley: float = 100.0,
                 spacing: float = 0.0,
                 angle: float = 0.0,
                 borderstyle: int = 1,
                 outline: float = 2.0,
                 shadow: float = 2.0,
                 alignment: int = 2,
                 marginl: int = 10,
                 marginr: int = 10,
                 marginv: int = 10,
                 alphalevel: int = 0,
                 encoding: int = 1):
        self.fontname: str = fontname  #: Font name
        self.fontsize: float = fontsize  #: Font size (in pixels)
        self.primarycolor: Color = primarycolor  #: Primary color (:class:`pysubs2.Color` instance)
        self.secondarycolor: Color = secondarycolor  #: Secondary color (:class:`pysubs2.Color` instance)
        self.tertiarycolor: Color = tertiarycolor  #: Tertiary color (:class:`pysubs2.Color` instance)
        self.outlinecolor: Color = outlinecolor  #: Outline color (:class:`pysubs2.Color` instance)
        self.backcolor: Color = backcolor  #: Back, ie. shadow color (:class:`pysubs2.Color` instance)
        self.bold: bool = bold  #: Bold
        self.italic: bool = italic  #: Italic
        self.underline: bool = underline  #: Underline (ASS only)
        self.strikeout: bool = strikeout  #: Strikeout (ASS only)
        self.scalex: float = scalex  #: Horizontal scaling (ASS only)
        self.scaley: float = scaley  #: Vertical scaling (ASS only)
        self.spacing: float = spacing  #: Letter spacing (ASS only)
        self.angle: float = angle  #: Rotation (ASS only)
        self.borderstyle: int = borderstyle  #: Border style
        self.outline: float = outline  #: Outline width (in pixels)
        self.shadow: float = shadow  #: Shadow depth (in pixels)
        self.alignment: int = alignment  #: Numpad-style alignment, eg. 7 is "top left" (that is, ASS alignment semantics)
        self.marginl: int = marginl  #: Left margin (in pixels)
        self.marginr: int = marginr  #: Right margin (in pixels)
        self.marginv: int = marginv  #: Vertical margin (in pixels)
        self.alphalevel: int = alphalevel  #: Old, unused SSA-only field
        self.encoding: int = encoding  #: Charset

        # The following attributes cannot be defined for SSA styles themselves,
        # but can be used in override tags and thus are useful to keep here
        # for the `pysubs2.substation.parse_tags()` interface which returns
        # SSAStyles for text fragments.
        self.drawing: bool = False  #: Drawing (ASS only override tag, see http://docs.aegisub.org/3.1/ASS_Tags/#drawing-tags)

    def copy(self) -> "SSAStyle":
        return SSAStyle(**self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return {field: getattr(self, field) for field in self.FIELDS}

    def __eq__(self, other: "SSAStyle"):
        return self.as_dict() == other.as_dict()

    def __ne__(self, other: "SSAStyle"):
        return not self == other

    def __repr__(self):
        return f"<SSAStyle {self.fontsize!r}px" \
               f"{' bold' if self.bold else ''}" \
               f"{' italic' if self.italic else ''}" \
               f" {self.fontname!r}>"


SSAStyle.DEFAULT_STYLE = SSAStyle()

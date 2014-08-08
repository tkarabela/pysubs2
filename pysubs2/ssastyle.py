from .common import Color


class SSAStyle(object):
    DEFAULT_STYLE = None

    FIELDS = frozenset([
        "fontname", "fontsize", "primarycolor", "secondarycolor",
        "tertiarycolor", "outlinecolor", "backcolor",
        "bold", "italic", "underline", "strikeout",
        "scalex", "scaley", "spacing", "angle", "borderstyle",
        "outline", "shadow", "alignment",
        "marginl", "marginr", "marginv", "alphalevel", "encoding"
    ])

    def __init__(self, **fields):
        self.fontname = "Arial"
        self.fontsize = 20.0
        self.primarycolor = Color(255, 255, 255, 0)
        self.secondarycolor = Color(255, 0, 0, 0)
        self.tertiarycolor = Color(0, 0, 0, 0)
        self.outlinecolor = Color(0, 0, 0, 0)
        self.backcolor = Color(0, 0, 0, 0)
        self.bold = False
        self.italic = False
        self.underline = False # ASS only
        self.strikeout = False # ASS only
        self.scalex = 100.0 # ASS only
        self.scaley = 100.0 # ASS only
        self.spacing = 0.0 # ASS only
        self.angle = 0.0 # ASS only
        self.borderstyle = 1
        self.outline = 2.0
        self.shadow = 2.0
        self.alignment = 2 # ASS semantics, SSA is different
        self.marginl = 10
        self.marginr = 10
        self.marginv = 10
        self.alphalevel = 0 # unused in SSA, not present in ASS...
        self.encoding = 1

        for k, v in fields.items():
            if k in self.FIELDS:
                setattr(self, k, v)
            else:
                raise ValueError("SSAStyle has no field named %r" % k)

    def copy(self):
        return SSAStyle(**{k: getattr(self, k) for k in self.FIELDS})

    def __eq__(self, other):
        # XXX document this
        return all(getattr(self, k) == getattr(other, k) for k in self.FIELDS)

    def __ne__(self, other):
        return not self == other


SSAStyle.DEFAULT_STYLE = SSAStyle()

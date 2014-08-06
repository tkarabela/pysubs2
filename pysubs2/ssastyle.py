from .common import Color


class SSAStyle(object):
    DEFAULT_VALUES = {
        "fontname": "Arial",
        "fontsize": 20.0,
        "primarycolor": Color(255, 255, 255, 0),
        "secondarycolor": Color(255, 0, 0, 0),
        "tertiarycolor": Color(0, 0, 0, 0),
        "outlinecolor": Color(0, 0, 0, 0),
        "backcolor": Color(0, 0, 0, 0),
        "bold": False,
        "italic": False,
        "underline": False, # ASS only
        "strikeout": False, # ASS only
        "scalex": 100.0, # ASS only
        "scaley": 100.0, # ASS only
        "spacing": 0.0, # ASS only
        "angle": 0.0, # ASS only
        "borderstyle": 1,
        "outline": 2.0,
        "shadow": 2.0,
        "alignment": 2, # ASS semantics, SSA is different
        "marginl": 10,
        "marginr": 10,
        "marginv": 10,
        "alphalevel": 0, # unused in SSA, not present in ASS...
        "encoding": 1}

    def __init__(self, **fields):
        for k, v in self.DEFAULT_VALUES.items():
            setattr(self, k, v)

        for k, v in fields.items():
            if k in self.DEFAULT_VALUES:
                setattr(self, k, v)
            else:
                raise ValueError("No field named %r" % k)

    def copy(self):
        s = SSAStyle()
        for k in self.DEFAULT_VALUES:
            setattr(s, k, getattr(self, k))
        return s

    def __eq__(self, other):
        # XXX document this
        return all(getattr(self, k) == getattr(other, k) for k in self.DEFAULT_VALUES)

    def __ne__(self, other):
        return not self == other

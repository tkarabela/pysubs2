class SSAEvent(object):
    """A SubStation Event, ie. one subtitle"""

    FIELDS = frozenset([
        "start", "end", "text", "marked", "layer", "style",
        "name", "marginl", "marginr", "marginv", "effect", "type"
    ])

    def __init__(self, **fields):
        self.start = 0 #: Subtitle start time (in milliseconds)
        self.end = 10000 #: Subtitle end time (in milliseconds)
        self.text = "" #: Text of subtitle (with SubStation override tags)
        self.marked = False #: (SSA only)
        self.layer = 0 #: Layer number, 0 is the lowest layer (ASS only)
        self.style = "Default" #: Style name
        self.name = "" #: Actor name
        self.marginl = 0 #: Left margin
        self.marginr = 0 #: Right margin
        self.marginv = 0 #: Vertical margin
        self.effect = "" #: Line effect
        self.type = "Dialogue" #: Line type (Dialogue/Comment)

        for k, v in fields.items():
            if k in self.FIELDS:
                setattr(self, k, v)
            else:
                raise ValueError("SSAEvent has no field named %r" % k)

    @property
    def duration(self):
        """Subtitle duration (in milliseconds)"""
        return self.end - self.start

    @duration.setter
    def duration(self, ms):
        if ms >= 0:
            self.end = self.start + ms
        else:
            raise ValueError("Subtitle duration cannot be negative")

    @property
    def is_comment(self):
        return self.type == "Comment"

    @is_comment.setter
    def is_comment(self, value):
        if value:
            self.type = "Comment"
        else:
            self.type = "Dialogue"

    def copy(self):
        return SSAEvent(**{k: getattr(self, k) for k in self.FIELDS})

    def equals(self, other):
        """Field-based equality for SSAEvents"""
        if isinstance(other, SSAEvent):
            return all(getattr(self, k) == getattr(other, k) for k in self.FIELDS)
        else:
            raise TypeError("Cannot compare to non-SSAEvent object")

    def __eq__(self, other):
        # XXX document this
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end

    def __lt__(self, other):
        return (self.start, self.end) < (other.start, other.end)

    def __le__(self, other):
        return (self.start, self.end) <= (other.start, other.end)

    def __gt__(self, other):
        return (self.start, self.end) > (other.start, other.end)

    def __ge__(self, other):
        return (self.start, self.end) >= (other.start, other.end)

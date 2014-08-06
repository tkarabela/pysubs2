from functools import total_ordering


@total_ordering
class SSAEvent(object):
    DEFAULT_VALUES = {
        "start": 0,
        "end": 10000,
        "text": "",
        "marked": False, # SSA only
        "layer": 0, # ASS only
        "style": "Default",
        "name": "",
        "marginl": 0,
        "marginr": 0,
        "marginv": 0,
        "effect": "",
        "type": "Dialogue"}

    def __init__(self, **fields):
        for k, v in self.DEFAULT_VALUES.items():
            setattr(self, k, v)

        for k, v in fields.items():
            if k in self.DEFAULT_VALUES:
                setattr(self, k, v)
            else:
                raise ValueError("No field named %r" % k)

    @property
    def duration(self):
        return self.end - self.start

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
        e = SSAEvent()
        for k in self.DEFAULT_VALUES:
            setattr(e, k, getattr(self, k))
        return e

    def __eq__(self, other):
        # XXX document this
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return (self.start, self.end) < (other.start, other.end)

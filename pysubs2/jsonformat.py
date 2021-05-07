import json
from .common import Color
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .formatbase import FormatBase


class JSONFormat(FormatBase):
    """
    Implementation of JSON subtitle pseudo-format (serialized pysubs2 internal representation)

    This is essentially SubStation Alpha as JSON.
    """
    @classmethod
    def guess_format(cls, text):
        """See :meth:`pysubs2.formats.FormatBase.guess_format()`"""
        if text.startswith("{\""):
            return "json"

    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        """See :meth:`pysubs2.formats.FormatBase.from_file()`"""
        data = json.load(fp)

        subs.info.clear()
        subs.info.update(data["info"])

        subs.styles.clear()
        for name, fields in data["styles"].items():
            subs.styles[name] = sty = SSAStyle()
            for k, v in fields.items():
                if "color" in k:
                    setattr(sty, k, Color(*v))
                else:
                    setattr(sty, k, v)

        subs.events = [SSAEvent(**fields) for fields in data["events"]]

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        """See :meth:`pysubs2.formats.FormatBase.to_file()`"""
        data = {
            "info": dict(**subs.info),
            "styles": {name: sty.as_dict() for name, sty in subs.styles.items()},
            "events": [ev.as_dict() for ev in subs.events]
        }

        json.dump(data, fp)

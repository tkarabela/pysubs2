__all__ = [
    "PossibleMissedSubtitleWarning",
    "Pysubs2Warning",
    "SubtitleAttributeWarning",
    "TimestampOverflow",
    "TimestampUnderflow",
]


class Pysubs2Warning(UserWarning):
    """Base class for pysubs2 warnings."""


class PossibleMissedSubtitleWarning(Pysubs2Warning):
    """The parser suspects that a subtitle was skipped due to being too malformed"""


class SubtitleAttributeWarning(Pysubs2Warning):
    """Generic warning related to a subtitle event attribute"""


class TimestampOverflow(SubtitleAttributeWarning):
    """During saving, a timestamp was greater than what the output format allows, it was clamped to maximum value"""


class TimestampUnderflow(SubtitleAttributeWarning):
    """During saving, a timestamp negative, it was clamped to zero"""

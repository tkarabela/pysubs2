__all__ = [
    "PossibleMissedSubtitleWarning",
    "Pysubs2Warning",
]


class Pysubs2Warning(UserWarning):
    """Base class for pysubs2 warnings."""


class PossibleMissedSubtitleWarning(Pysubs2Warning):
    pass

class Pysubs2Error(Exception):
    """Base class for pysubs2 exceptions."""


class UnknownFPSError(Pysubs2Error):
    """Framerate was not specified and couldn't be inferred otherwise."""

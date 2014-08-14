from .formatbase import FormatBase
from .microdvd import MicroDVDFormat
from .subrip import SubripFormat
from .jsonformat import JSONFormat


FILE_EXTENSION_TO_FORMAT_IDENTIFIER = {
    ".srt": "srt",
    ".ass": "ass",
    ".ssa": "ssa",
    ".sub": "microdvd",
    ".json": "json"
}

FORMAT_IDENTIFIER_TO_FORMAT_CLASS = {
    "srt": SubripFormat,
    "ass": FormatBase,
    "ssa": FormatBase,
    "microdvd": MicroDVDFormat,
    "json": JSONFormat
}

def get_format_class(format_):
    # XXX throw specific exception
    return FORMAT_IDENTIFIER_TO_FORMAT_CLASS[format_]

def get_format_identifier(ext):
    # XXX throw specific exception
    return FILE_EXTENSION_TO_FORMAT_IDENTIFIER[ext]

def autodetect_format(content):
    formats = set()
    for impl in FORMAT_IDENTIFIER_TO_FORMAT_CLASS.values():
        guess = impl.guess_format(content)
        if guess is not None:
            formats.add(guess)

    if len(formats) == 1:
        return formats.pop()
    elif not formats:
        raise ValueError("No suitable formats")
    else:
        raise ValueError("Multiple suitable formats") # XXX raise sth better

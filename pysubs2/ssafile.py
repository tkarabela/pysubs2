# mypy: disable-error-code="no-overload-impl,overload-cannot-match,no-redef"

import io
import logging
from collections.abc import Iterable, Iterator, MutableSequence
from itertools import chain
from pathlib import Path
from typing import Any, ClassVar, Literal, TextIO, Unpack, overload, override

from .common import IntOrFloat, PathOrStr
from .formats.jsonformat import JSONFormat
from .formats.microdvd import MicroDVDFormat
from .formats.mpl2 import MPL2Format
from .formats.sami import SAMIFormat
from .formats.subrip import SubripFormat
from .formats.substation import SubstationFormat
from .formats.tmp import TmpFormat
from .formats.ttml import TTMLFormat
from .formats.webvtt import WebVTTFormat
from .formats.whisper import WhisperJAXFormat
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .time import make_time, ms_to_str

logger = logging.getLogger(__name__)


class SSAFile(MutableSequence[SSAEvent]):
    """
    Subtitle file in SubStation Alpha format.

    This class has a list-like interface which exposes :attr:`SSAFile.events`,
    list of subtitles in the file::

        subs = SSAFile.load("subtitles.srt")

        for line in subs:
            print(line.text)

        subs.insert(0, SSAEvent(start=0, end=make_time(s=2.5), text="New first subtitle"))

        del subs[0]

    Attributes:
        events: List of :class:`SSAEvent` instances, ie. individual subtitles.
        styles: Dict of :class:`SSAStyle` instances.
        info: Dict with script metadata, ie. ``[Script Info]``.
        aegisub_project: Dict with Aegisub project, ie. ``[Aegisub Project Garbage]``.
        fonts_opaque: Dict with embedded fonts, ie. ``[Fonts]``.
        graphics_opaque: Dict with embedded images, ie. ``[Graphics]``.
        fps: Framerate used when reading the file, if applicable.
        format: Format of source subtitle file, if applicable, eg. ``"srt"``.

    """

    DEFAULT_INFO: ClassVar[dict[str, str]] = {
        "WrapStyle": "0",
        "ScaledBorderAndShadow": "yes",
        "Collisions": "Normal"
    }
    events: list[SSAEvent]
    styles: dict[str, SSAStyle]
    info: dict[str, str]
    aegisub_project: dict[str, str]
    fonts_opaque: dict[str, Any]
    graphics_opaque: dict[str, Any]
    fps: float | None
    format: str | None

    def __init__(self) -> None:
        self.events = []
        self.styles = {"Default": SSAStyle.DEFAULT_STYLE.copy()}
        self.info = self.DEFAULT_INFO.copy()
        self.aegisub_project = {}
        self.fonts_opaque = {}
        self.graphics_opaque = {}
        self.fps = None
        self.format = None

    # ------------------------------------------------------------------------
    # I/O methods - overloads per format
    # ------------------------------------------------------------------------

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: str | None = None,
            errors: str | None = None
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["json"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[JSONFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["microdvd"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[MicroDVDFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["mpl2"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[MPL2Format.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["sami"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[SAMIFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["srt"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[SubripFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["ass", "ssa"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[SubstationFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["tmp"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[TmpFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["ttml"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[TTMLFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["vtt"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[WebVTTFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def load(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["whisper_jax"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[WhisperJAXFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: str | None = None,
            **kwargs: Any
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["json"] | str | None = None,
            **kwargs: Unpack[JSONFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["microdvd"] | str | None = None,
            **kwargs: Unpack[MicroDVDFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["mpl2"] | str | None = None,
            **kwargs: Unpack[MPL2Format.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["sami"] | str | None = None,
            **kwargs: Unpack[SAMIFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["srt"] | str | None = None,
            **kwargs: Unpack[SubripFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["ass", "ssa"] | str | None = None,
            **kwargs: Unpack[SubstationFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["tmp"] | str | None = None,
            **kwargs: Unpack[TmpFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["ttml"] | str | None = None,
            **kwargs: Unpack[TTMLFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["vtt"] | str | None = None,
            **kwargs: Unpack[WebVTTFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_string(
            cls,
            string: str,
            format_: Literal["whisper_jax"] | str | None = None,
            **kwargs: Unpack[WhisperJAXFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: str | None = None,
            **kwargs: Any
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["json"] | str | None = None,
            **kwargs: Unpack[JSONFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["microdvd"] | str | None = None,
            **kwargs: Unpack[MicroDVDFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["mpl2"] | str | None = None,
            **kwargs: Unpack[MPL2Format.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["sami"] | str | None = None,
            **kwargs: Unpack[SAMIFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["srt"] | str | None = None,
            **kwargs: Unpack[SubripFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["ass", "ssa"] | str | None = None,
            **kwargs: Unpack[SubstationFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["tmp"] | str | None = None,
            **kwargs: Unpack[TmpFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["ttml"] | str | None = None,
            **kwargs: Unpack[TTMLFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["vtt"] | str | None = None,
            **kwargs: Unpack[WebVTTFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    @classmethod
    def from_file(
            cls,
            fp: TextIO,
            format_: Literal["whisper_jax"] | str | None = None,
            **kwargs: Unpack[WhisperJAXFormat.ReaderArgs]
    ) -> "SSAFile":
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: str | None = None,
            errors: str | None = None,
            **kwargs: Any
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["json"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[JSONFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["microdvd"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[MicroDVDFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["mpl2"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[MPL2Format.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["srt"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[SubripFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["ass", "ssa"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[SubstationFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["tmp"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[TmpFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["ttml"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[TTMLFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def save(
            cls,
            path: PathOrStr,
            encoding: str = "utf-8",
            format_: Literal["vtt"] | str | None = None,
            errors: str | None = None,
            **kwargs: Unpack[WebVTTFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_string(
            cls,
            format_: str,
            **kwargs: Any
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["json"] | str,
            **kwargs: Unpack[JSONFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["microdvd"] | str,
            **kwargs: Unpack[MicroDVDFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["mpl2"] | str,
            **kwargs: Unpack[MPL2Format.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["srt"] | str,
            **kwargs: Unpack[SubripFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["ass", "ssa"] | str,
            **kwargs: Unpack[SubstationFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["tmp"] | str,
            **kwargs: Unpack[TmpFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["ttml"] | str,
            **kwargs: Unpack[TTMLFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_string(
            cls,
            format_: Literal["vtt"] | str,
            **kwargs: Unpack[WebVTTFormat.WriterArgs]
    ) -> str:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: str,
            **kwargs: Any
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["json"] | str,
            **kwargs: Unpack[JSONFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["microdvd"] | str,
            **kwargs: Unpack[MicroDVDFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["mpl2"] | str,
            **kwargs: Unpack[MPL2Format.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["srt"] | str,
            **kwargs: Unpack[SubripFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["ass", "ssa"] | str,
            **kwargs: Unpack[SubstationFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["tmp"] | str,
            **kwargs: Unpack[TmpFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["ttml"] | str,
            **kwargs: Unpack[TTMLFormat.WriterArgs]
    ) -> None:
        pass

    @overload
    def to_file(
            cls,
            fp: TextIO,
            format_: Literal["vtt"] | str,
            **kwargs: Unpack[WebVTTFormat.WriterArgs]
    ) -> None:
        pass

    # ------------------------------------------------------------------------
    # I/O methods - actual implementation
    # ------------------------------------------------------------------------

    @classmethod
    def load(cls, path: PathOrStr, encoding: str = "utf-8", format_: str | None = None,
             errors: str | None = None, **kwargs: Any) -> "SSAFile":
        """
        Load subtitle file from given path.

        This method is implemented in terms of :meth:`SSAFile.from_file()`.

        See also:
            Specific formats may implement additional loading options,
            please refer to documentation of the implementation classes
            (eg. :meth:`pysubs2.formats.subrip.SubripFormat.from_file()`)

        Arguments:
            path (Path | str): Path to subtitle file.
            encoding (str): Character encoding of input file.
                Defaults to UTF-8, you may need to change this.
            errors (str | None): Error handling for character encoding
                of input file. Defaults to ``None``; use the value ``"surrogateescape"``
                for pass-through of bytes not supported by selected encoding via
                `Unicode surrogate pairs <https://en.wikipedia.org/wiki/Universal_Character_Set_characters#Surrogates>`_.
                See documentation of builtin ``open()`` function for more.

                .. versionchanged:: 1.7.0
                    The ``errors`` parameter was introduced to facilitate
                    pass-through of subtitle files with unknown text encoding.
                    Previous versions of the library behaved as if ``errors=None``.

            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file contents. This argument should
                be rarely needed.
            fps (float): Framerate for frame-based formats (MicroDVD),
                for other formats this argument is ignored. Framerate might
                be detected from the file, in which case you don't need
                to specify it here (when given, this argument overrides
                autodetection).
            kwargs: Extra options for the reader.

        Returns:
            SSAFile

        Raises:
            IOError
            UnicodeDecodeError
            pysubs2.exceptions.UnknownFPSError
            pysubs2.exceptions.UnknownFormatIdentifierError
            pysubs2.exceptions.FormatAutodetectionError

        Note:
            pysubs2 may autodetect subtitle format and/or framerate. These
            values are set as :attr:`SSAFile.format` and :attr:`SSAFile.fps`
            attributes.

        Example:
            >>> subs1 = pysubs2.load("subrip-subtitles.srt")
            >>> subs2 = pysubs2.load("microdvd-subtitles.sub", fps=23.976)
            >>> subs3 = pysubs2.load("subrip-subtitles-with-fancy-tags.srt", keep_unknown_html_tags=True)

        """
        with Path(path).open(encoding=encoding, errors=errors) as fp:
            return cls.from_file(fp, format_, **kwargs)

    @classmethod
    def from_string(cls, string: str, format_: str | None = None,
                    **kwargs: Any) -> "SSAFile":
        """
        Load subtitle file from string.

        See :meth:`SSAFile.load()` for full description.

        Arguments:
            string (str): Subtitle file in a string. Note that the string must be Unicode (``str``, not ``bytes``).
            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file contents. This argument should
                be rarely needed.
            fps (float): Framerate for frame-based formats (MicroDVD),
                for other formats this argument is ignored. Framerate might
                be detected from the file, in which case you don't need
                to specify it here (when given, this argument overrides
                autodetection).

        Returns:
            SSAFile

        Example:
            >>> text = '''
            ... 1
            ... 00:00:00,000 --> 00:00:05,000
            ... An example SubRip file.
            ... '''
            >>> subs = SSAFile.from_string(text)

        """
        fp = io.StringIO(string)
        return cls.from_file(fp, format_, **kwargs)

    @classmethod
    def from_file(cls, fp: TextIO, format_: str | None = None,
                  **kwargs: Any) -> "SSAFile":
        """
        Read subtitle file from file object.

        See :meth:`SSAFile.load()` for full description.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.load()`
            or :meth:`SSAFile.from_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`TextIO` instance.
                Note that the file must be opened in text mode (as opposed to binary).
            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file contents. This argument should
                be rarely needed.
            fps (float): Framerate for frame-based formats (MicroDVD),
                for other formats this argument is ignored. Framerate might
                be detected from the file, in which case you don't need
                to specify it here (when given, this argument overrides
                autodetection).

        Returns:
            SSAFile

        """
        from .formats import autodetect_format, get_format_class

        if format_ is None:
            # Autodetect subtitle format, then read again using correct parser.
            # The file might be a pipe and we need to read it twice,
            # so just buffer everything.
            text = fp.read()
            fragment = text[:10000]
            format_ = autodetect_format(fragment)
            fp = io.StringIO(text)

        impl = get_format_class(format_)
        subs = cls() # an empty subtitle file
        subs.format = format_
        impl.from_file(subs, fp, format_, **kwargs)
        return subs

    def save(self, path: PathOrStr, encoding: str = "utf-8", format_: str | None = None,
             errors: str | None = None, **kwargs: Any) -> None:
        """
        Save subtitle file to given path.

        This method is implemented in terms of :meth:`SSAFile.to_file()`.

        See also:
            Specific formats may implement additional saving options,
            please refer to documentation of the implementation classes
            (eg. :meth:`pysubs2.formats.subrip.SubripFormat.to_file()`)

        Arguments:
            path (Path | str): Path to subtitle file.
            encoding (str): Character encoding of output file.
                Defaults to UTF-8, which should be fine for most purposes.
            format_ (str): Optional, specifies desired subtitle format
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file extension. Thus, this argument
                is rarely needed.
            fps (float): Framerate for frame-based formats (MicroDVD),
                for other formats this argument is ignored. When omitted,
                :attr:`SSAFile.fps` value is used (ie. the framerate used
                for loading the file, if any). When the :class:`SSAFile`
                wasn't loaded from MicroDVD, or if you wish save it with
                different framerate, use this argument. See also
                :meth:`SSAFile.transform_framerate()` for fixing bad
                frame-based to time-based conversions.
            errors (str | None): Error handling for character encoding
                of input file. Defaults to ``None``; use the value ``"surrogateescape"``
                for pass-through of bytes not supported by selected encoding via
                `Unicode surrogate pairs <https://en.wikipedia.org/wiki/Universal_Character_Set_characters#Surrogates>`_.
                See documentation of builtin ``open()`` function for more.

                .. versionchanged:: 1.7.0
                    The ``errors`` parameter was introduced to facilitate
                    pass-through of subtitle files with unknown text encoding.
                    Previous versions of the library behaved as if ``errors=None``.

            kwargs: Extra options for the writer.

        Raises:
            IOError
            UnicodeEncodeError
            pysubs2.exceptions.UnknownFPSError
            pysubs2.exceptions.UnknownFormatIdentifierError
            pysubs2.exceptions.UnknownFileExtensionError

        """
        outpath = Path(path)
        if format_ is None:
            from .formats import get_format_identifier

            ext = outpath.suffix.lower()
            format_ = get_format_identifier(ext)

        with outpath.open("w", encoding=encoding, errors=errors) as fp:
            self.to_file(fp, format_, **kwargs)

    def to_string(self, format_: str, **kwargs: Any) -> str:
        """
        Get subtitle file as a string.

        See :meth:`SSAFile.save()` for full description.

        Returns:
            str

        """
        fp = io.StringIO()
        self.to_file(fp, format_, **kwargs)
        return fp.getvalue()

    def to_file(self, fp: TextIO, format_: str, **kwargs: Any) -> None:
        """
        Write subtitle file to file object.

        See :meth:`SSAFile.save()` for full description.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.save()`
            or :meth:`SSAFile.to_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`TextIO` instance.
                Note that the file must be opened in text mode (as opposed to binary).

        """
        from .formats import get_format_class

        impl = get_format_class(format_)
        impl.to_file(self, fp, format_, **kwargs)

    # ------------------------------------------------------------------------
    # Retiming subtitles
    # ------------------------------------------------------------------------

    def shift(self, h: IntOrFloat = 0, m: IntOrFloat = 0, s: IntOrFloat = 0, ms: IntOrFloat = 0,
              frames: int | None = None, fps: float | None = None) -> None:
        """
        Shift all subtitles by constant time amount.

        Shift may be time-based (the default) or frame-based. In the latter
        case, specify both frames and fps. h, m, s, ms will be ignored.

        Arguments:
            h: Integer or float values, may be positive or negative (hours).
            m: Integer or float values, may be positive or negative (minutes).
            s: Integer or float values, may be positive or negative (seconds).
            ms: Integer or float values, may be positive or negative (milliseconds).
            frames (int): When specified, must be an integer number of frames.
                May be positive or negative. fps must be also specified.
            fps (float): When specified, must be a positive number.

        Raises:
            ValueError: Invalid fps or missing number of frames.

        """
        delta = make_time(h=h, m=m, s=s, ms=ms, frames=frames, fps=fps)
        for line in self:
            line.start += delta
            line.end += delta

    def transform_framerate(self, in_fps: float, out_fps: float) -> None:
        """
        Rescale all timestamps by ratio of in_fps/out_fps.

        Can be used to fix files converted from frame-based to time-based
        with wrongly assumed framerate.

        Arguments:
            in_fps (float)
            out_fps (float)

        Raises:
            ValueError: Non-positive framerate given.

        """
        if in_fps <= 0 or out_fps <= 0:
            raise ValueError(f"Framerates must be positive, cannot transform {in_fps} -> {out_fps}")

        ratio = in_fps / out_fps
        for line in self:
            line.start = int(round(line.start * ratio))
            line.end = int(round(line.end * ratio))

    # ------------------------------------------------------------------------
    # Working with styles
    # ------------------------------------------------------------------------

    def rename_style(self, old_name: str, new_name: str) -> None:
        """
        Rename a style, including references to it.

        Arguments:
            old_name (str): Style to be renamed.
            new_name (str): New name for the style (must be unused).

        Raises:
            KeyError: No style named old_name.
            ValueError: new_name is not a legal name (cannot use commas)
                or new_name is taken.

        """
        from .formats.substation import is_valid_field_content

        if old_name not in self.styles:
            raise KeyError(f"Style {old_name!r} not found")
        if new_name in self.styles:
            raise ValueError(f"There is already a style called {new_name!r}")
        if not is_valid_field_content(new_name):
            raise ValueError(f"{new_name!r} is not a valid name")

        self.styles[new_name] = self.styles[old_name]
        del self.styles[old_name]

        for line in self:
            # XXX also handle \r override tag
            if line.style == old_name:
                line.style = new_name

    def import_styles(self, subs: "SSAFile", overwrite: bool = True) -> None:
        """
        Merge in styles from other SSAFile.

        Arguments:
            subs (SSAFile): Subtitle file imported from.
            overwrite (bool): On name conflict, use style from the other file
                (default: True).

        """
        if not isinstance(subs, SSAFile):
            raise TypeError("Must supply an SSAFile.")

        for name, style in subs.styles.items():
            if name not in self.styles or overwrite:
                self.styles[name] = style

    # ------------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------------

    def remove_miscellaneous_events(self) -> None:
        """
        Remove subtitles which appear to be non-essential (the --clean in CLI)

        Currently, this removes events matching any of these criteria:
        - SSA event type Comment
        - SSA drawing tags
        - Less than two characters of text
        - Duplicated text with identical time interval (only the first event is kept)
        """
        new_events: list[SSAEvent] = []

        duplicate_text_ids: set[int] = set()
        times_to_texts: dict[tuple[int, int], list[str]] = {}

        for i, e in enumerate(self):
            tmp = times_to_texts.setdefault((e.start, e.end), [])
            if tmp.count(e.plaintext) > 0:
                duplicate_text_ids.add(i)
            tmp.append(e.plaintext)

        for i, e in enumerate(self):
            if e.is_drawing or e.is_comment:
                continue
            if len(e.plaintext.strip()) < 2:
                continue
            if i in duplicate_text_ids:
                continue

            new_events.append(e)

        self.events = new_events

    def get_text_events(self) -> list[SSAEvent]:
        """
        Return list of events excluding SSA comment lines and lines with SSA drawing tags
        """
        return [e for e in self if e.is_text]

    def equals(self, other: "SSAFile") -> bool:
        """
        Equality of two SSAFiles.

        Compares :attr:`SSAFile.info`, :attr:`SSAFile.styles` and :attr:`SSAFile.events`.
        Order of entries in OrderedDicts does not matter. "ScriptType" key in info is
        considered an implementation detail and thus ignored.

        Useful mostly in unit tests. Differences are logged at DEBUG level.

        """

        if isinstance(other, SSAFile):
            for key in set(chain(self.info.keys(), other.info.keys())) - {"ScriptType"}:
                self_info, other_info = self.info.get(key), other.info.get(key)
                if self_info is None:
                    logger.debug("%r missing in self.info", key)
                    return False
                elif other_info is None:
                    logger.debug("%r missing in other.info", key)
                    return False
                elif self_info != other_info:
                    logger.debug("info %r differs (self=%r, other=%r)", key, self_info, other_info)
                    return False

            for key in set(chain(self.fonts_opaque.keys(), other.fonts_opaque.keys())):
                self_font, other_font = self.fonts_opaque.get(key), other.fonts_opaque.get(key)
                if self_font is None:
                    logger.debug("%r missing in self.fonts_opaque", key)
                    return False
                elif other_font is None:
                    logger.debug("%r missing in other.fonts_opaque", key)
                    return False
                elif self_font != other_font:
                    logger.debug("fonts_opaque %r differs (self=%r, other=%r)", key, self_font, other_font)
                    return False

            for key in set(chain(self.graphics_opaque.keys(), other.graphics_opaque.keys())):
                self_image, other_image = self.graphics_opaque.get(key), other.graphics_opaque.get(key)
                if self_image is None:
                    logger.debug("%r missing in self.graphics_opaque", key)
                    return False
                elif other_image is None:
                    logger.debug("%r missing in other.graphics_opaque", key)
                    return False
                elif self_image != other_image:
                    logger.debug("graphics_opaque %r differs (self=%r, other=%r)", key, self_image, other_image)
                    return False

            for key in set(chain(self.styles.keys(), other.styles.keys())):
                self_style, other_style = self.styles.get(key), other.styles.get(key)
                if self_style is None:
                    logger.debug("%r missing in self.styles", key)
                    return False
                elif other_style is None:
                    logger.debug("%r missing in other.styles", key)
                    return False
                elif self_style != other_style:
                    for k in self_style.FIELDS:
                        if getattr(self_style, k) != getattr(other_style, k):
                            logger.debug("difference in field %r", k)
                    logger.debug("style %r differs (self=%r, other=%r)", key, self_style.as_dict(), other_style.as_dict())
                    return False

            if len(self) != len(other):
                logger.debug("different # of subtitles (self=%d, other=%d)", len(self), len(other))
                return False

            for i, (self_event, other_event) in enumerate(zip(self.events, other.events)):
                if not self_event.equals(other_event):
                    for k in self_event.FIELDS:
                        if getattr(self_event, k) != getattr(other_event, k):
                            logger.debug("difference in field %r", k)
                    logger.debug("event %d differs (self=%r, other=%r)", i, self_event.as_dict(), other_event.as_dict())
                    return False

            return True
        else:
            raise TypeError("Cannot compare to non-SSAFile object")

    def __repr__(self) -> str:
        if self.events:
            max_time = max(ev.end for ev in self)
            s = f"<SSAFile with {len(self)} events and {len(self.styles)} styles, last timestamp {ms_to_str(max_time)}>"
        else:
            s = f"<SSAFile with 0 events and {len(self.styles)} styles>"

        return s

    # ------------------------------------------------------------------------
    # MutableSequence implementation + sort()
    # ------------------------------------------------------------------------

    def sort(self) -> None:
        """Sort subtitles time-wise, in-place."""
        self.events.sort()

    @override
    def __iter__(self) -> Iterator[SSAEvent]:
        return iter(self.events)

    @overload
    def __getitem__(self, item: int) -> SSAEvent:
        pass

    @overload
    def __getitem__(self, item: slice) -> list[SSAEvent]:
        pass

    @override
    def __getitem__(self, item: Any) -> Any:
        return self.events[item]

    @overload
    def __setitem__(self, key: int, value: SSAEvent) -> None:
        pass

    @overload
    def __setitem__(self, key: slice, value: Iterable[SSAEvent]) -> None:
        pass

    @override
    def __setitem__(self, key: Any, value: Any) -> None:
        if isinstance(key, int):
            if isinstance(value, SSAEvent):
                self.events[key] = value
            else:
                raise TypeError("SSAFile.events must contain only SSAEvent objects")
        elif isinstance(key, slice):
            values = list(value)
            if all(isinstance(v, SSAEvent) for v in values):
                self.events[key] = values
            else:
                raise TypeError("SSAFile.events must contain only SSAEvent objects")
        else:
            raise TypeError("Bad key type")

    @overload
    def __delitem__(self, key: int) -> None:
        pass

    @overload
    def __delitem__(self, key: slice) -> None:
        pass

    @override
    def __delitem__(self, key: Any) -> None:
        del self.events[key]

    @override
    def __len__(self) -> int:
        return len(self.events)

    @override
    def insert(self, index: int, value: SSAEvent) -> None:
        if isinstance(value, SSAEvent):
            self.events.insert(index, value)
        else:
            raise TypeError("SSAFile.events must contain only SSAEvent objects")

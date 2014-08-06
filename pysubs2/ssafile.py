"""
``SSAFile`` --- a subtitle file
===============================

.. autoclass:: pysubs2.SSAFile


Reading and writing subtitles
-----------------------------

Using file
~~~~~~~~~~

.. automethod:: SSAFile.load
.. automethod:: SSAFile.save

Using string
~~~~~~~~~~~~

.. automethod:: SSAFile.from_string
.. automethod:: SSAFile.to_string

Using file object
~~~~~~~~~~~~~~~~~

.. automethod:: SSAFile.from_file
.. automethod:: SSAFile.to_file

Retiming subtitles
------------------

.. automethod:: SSAFile.shift
.. automethod:: SSAFile.transform_framerate

Working with styles
-------------------

.. automethod:: SSAFile.rename_style
.. automethod:: SSAFile.import_styles

"""

from collections import MutableSequence, OrderedDict
import io
from io import open
import os.path
from .formats import autodetect_format, get_format_class, get_format_identifier
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from .time import make_time


class SSAFile(MutableSequence):
    """
    Subtitle file in SubStation Alpha format.

    """

    DEFAULT_STYLES = OrderedDict({"Default": SSAStyle()}.items())
    DEFAULT_INFO = OrderedDict(
        {"WrapStyle": "0",
         "ScaledBorderAndShadow": "yes",
         "Collisions": "Normal"}.items())

    def __init__(self):
        self.events = []
        self.styles = self.DEFAULT_STYLES.copy()
        self.info = self.DEFAULT_INFO.copy()
        self.fps = None
        self.format = None

    # ------------------------------------------------------------------------
    # I/O methods
    # ------------------------------------------------------------------------

    @classmethod
    def load(cls, path, encoding="utf-8", format_=None, fps=None, **kwargs):
        """
        Load subtitle file from given path.

        Arguments:
            path (str): Path to subtitle file.
            encoding (str): Character encoding of input file.
                Defaults to UTF-8, you may need to change this.
            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file contents. This argument should
                be rarely needed.
            fps (float): Framerate for frame-based formats (MicroDVD),
                for other formats this argument is ignored. Framerate might
                be detected from the file, in which case you don't need
                to specify it here (when given, this argument overrides
                autodetection).
            kwargs: Extra options for the parser.

        Returns:
            SSAFile

        Note:
            pysubs2 may autodetect subtitle format and/or framerate. These
            values are set as :attr:`SSAFile.format` and :attr:`SSAfile.fps`
            attributes.

        Example:
            >>> subs1 = pysubs2.load("subrip-subtitles.srt")
            >>> subs2 = pysubs2.load("microdvd-subtitles.sub", fps=23.976)

        """
        with open(path, encoding=encoding) as fp:
            return cls.from_file(fp, format_, fps=fps, **kwargs)

    @classmethod
    def from_string(cls, string, format_=None, fps=None, **kwargs):
        """
        Load subtitle file from string.

        See :meth:`SSAFile.load()` for full description.

        Arguments:
            string (str): Subtitle file in a string. Note that the string
                must be Unicode (in Python 2).

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
        return cls.from_file(fp, format_, fps=fps, **kwargs)

    @classmethod
    def from_file(cls, fp, format_=None, fps=None, **kwargs):
        """
        Read subtitle file from file object.

        See :meth:`SSAFile.load()` for full description.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.load()`
            or :meth:`SSAFile.from_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`io.TextIOBase` instance.
                Note that the file must be opened in text mode (as opposed to binary).

        Returns:
            SSAFile

        """
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
        subs.fps = fps
        return impl.from_file(subs, fp, format_, fps=fps, **kwargs)

    def save(self, path, encoding="utf-8", format_=None, fps=None, **kwargs):
        """
        Save subtitle file to given path.

        Arguments:
            path (str): Path to subtitle file.
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
            kwargs: Extra options for the writer.

        """
        if format_ is None:
            ext = os.path.splitext(path)[1].lower()
            format_ = get_format_identifier(ext)

        with open(path, "w", encoding=encoding) as fp:
            self.to_file(fp, format_, fps=fps, **kwargs)

    def to_string(self, format_, fps=None, **kwargs):
        """
        Get subtitle file as a string.

        See :meth:`SSAFile.save()` for full description.

        Returns:
            str

        """
        fp = io.StringIO()
        self.to_file(fp, format_, fps=fps, **kwargs)
        return fp.getvalue()

    def to_file(self, fp, format_, fps=None, **kwargs):
        """
        Write subtitle file to file object.

        See :meth:`SSAFile.save()` for full description.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.save()`
            or :meth:`SSAFile.to_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`io.TextIOBase` instance.
                Note that the file must be opened in text mode (as opposed to binary).

        """
        impl = get_format_class(format_)
        return impl.to_file(self, fp, format_, fps=fps, **kwargs)

    # ------------------------------------------------------------------------
    # Retiming subtitles
    # ------------------------------------------------------------------------

    def shift(self, h=0, m=0, s=0, ms=0, frames=None, fps=None):
        delta = make_time(h=h, m=m, s=s, ms=ms, frames=frames, fps=fps)
        for line in self:
            line.start += delta
            line.end += delta

    def transform_framerate(self, in_fps, out_fps):
        pass # XXX implement

    # ------------------------------------------------------------------------
    # Working with styles
    # ------------------------------------------------------------------------

    def rename_style(self, old_name, new_name):
        pass # XXX implement

    def import_styles(self, subs, overwrite=True):
        pass # XXX implement

    # ------------------------------------------------------------------------
    # MutableSequence implementation
    # ------------------------------------------------------------------------

    def __getitem__(self, item):
        return self.events[item]

    def __setitem__(self, key, value):
        if isinstance(value, SSAEvent):
            self.events[key] = value
        else:
            raise TypeError("SSAFile.events must contain only SSAEvent objects")

    def __delitem__(self, key):
        del self.events[key]

    def __len__(self):
        return len(self.events)

    def insert(self, index, value):
        if isinstance(value, SSAEvent):
            self.events.insert(index, value)
        else:
            raise TypeError("SSAFile.events must contain only SSAEvent objects")

from collections import MutableSequence, OrderedDict
import io
from io import open
import os.path
from .formats import autodetect_format, get_format_class, get_format_identifier
from .ssaevent import SSAEvent


class SSAFile(MutableSequence):
    """
    Subtitle file in SubStation Alpha format.

    """
    def __init__(self):
        self.events = []
        self.styles = OrderedDict()
        self.info = OrderedDict()

    # ------------------------------------------------------------------------
    # I/O methods
    # ------------------------------------------------------------------------

    @classmethod
    def load(cls, path, encoding="utf-8", format_=None, **kwargs):
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
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

        Returns:
            SSAFile
        """
        with open(path, encoding=encoding) as fp:
            return cls.from_file(fp, format_, **kwargs)

    @classmethod
    def from_string(cls, string, format_=None, **kwargs):
        """
        Load subtitle file from string.

        Arguments:
            string (str): Subtitle file in a string. Note that the string
                must be Unicode (in Python 2).
            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from content. This argument should
                be rarely needed.
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

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
    def from_file(cls, fp, format_=None, **kwargs):
        """
        Read subtitle file from file object.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.load()`
            or :meth:`SSAFile.from_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`io.TextIOBase` instance.
                Note that the file must be opened in text mode (as opposed to binary).
            encoding (str): Character encoding of input file.
                Defaults to UTF-8, you may need to change this.
            format_ (str): Optional, forces use of specific parser
                (eg. `"srt"`, `"ass"`). Otherwise, format is detected
                automatically from file contents. This argument should
                be rarely needed.
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

        Returns:
            SSAFile

        """
        if format_ is None:
            # Autodetect subtitle format, then read again using correct parser.
            # The file might be a pipe and we need to read it twice,
            # so just buffer everything.
            text = fp.read()
            format_ = autodetect_format(text)
            fp = io.StringIO(text)

        impl = get_format_class(format_)
        subs = cls() # an empty subtitle file
        return impl.from_file(subs, fp, format_, **kwargs)

    def save(self, path, encoding="utf-8", format_=None, **kwargs):
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
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

        """
        if format_ is None:
            ext = os.path.splitext(path)[1]
            format_ = get_format_identifier(ext)

        with open(path, "w", encoding=encoding) as fp:
            self.to_file(fp, format_, **kwargs)

    def to_string(self, format_, **kwargs):
        """
        Get subtitle file as a string.

        Arguments:
            format_ (str): Specifies desired subtitle format
                (eg. `"srt"`, `"ass"`).
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

        Returns:
            str

        """
        # XXX reconsider name of this method and other IO utility methods
        fp = io.StringIO()
        self.to_file(fp, format_, **kwargs)
        return fp.getvalue()

    def to_file(self, fp, format_, **kwargs):
        """
        Write subtitle file to file object.

        Note:
            This is a low-level method. Usually, one of :meth:`SSAFile.save()`
            or :meth:`SSAFile.to_string()` is preferable.

        Arguments:
            fp (file object): A file object, ie. :class:`io.TextIOBase` instance.
                Note that the file must be opened in text mode (as opposed to binary).
            format_ (str): Specifies desired subtitle format
                (eg. `"srt"`, `"ass"`).
            **kwargs: Format-specific settings, eg. `fps` for MicroDVD.

        """
        impl = get_format_class(format_)
        return impl.to_file(self, fp, format_, **kwargs)

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

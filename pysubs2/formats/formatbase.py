class FormatBase(object):
    """
    Base class for subtitle format implementations.
    """
    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        """
        Load subtitle file into empty SSAFile.

        If the parser autodetects framerate, set it as ``subs.fps``.

        Arguments:
            subs (SSAFile): An empty :class:`SSAFile`.
            fp (file object): Text file object, the subtitle file.
            format_ (str): Format identifier. Used when one format class
                implements multiple formats (see :class:`SubstationFormat`).
            kwargs: Extra options, eg. `fps`.

        Returns:
            None

        Raises:
            pysubs2.UnknownFPSError: Framerate was not provided and cannot
                be detected.
        """
        raise NotImplementedError("Parsing is not supported for this format")

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        """
        Write SSAFile into file.

        If you need framerate and it is not passed in keyword arguments,
        use ``subs.fps``.

        Arguments:
            subs (SSAFile): Subtitle file to write.
            fp (file object): Text file object used as output.
            format_ (str): Format identifier of desired output format.
                Used when one format class implements multiple formats
                (see :class:`SubstationFormat`).
            kwargs: Extra options, eg. `fps`.

        Returns:
            None

        Raises:
            pysubs2.UnknownFPSError: Framerate was not provided and
                ``subs.fps is None``.
        """
        raise NotImplementedError("Writing is not supported for this format")

    @classmethod
    def guess_format(self, text):
        """
        Return format identifier of recognized format, or None.

        Arguments:
            text (str): Content of subtitle file. When the file is long,
                this may be only its first few thousand characters.

        Returns:
            format identifier (eg. ``"srt"``) or None (unknown format)
        """
        return None

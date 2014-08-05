class FormatBase(object):
    @classmethod
    def from_file(cls, subs, fp, format_, **kwargs):
        raise NotImplementedError("Writing is not supported for this format")

    @classmethod
    def to_file(cls, subs, fp, format_, **kwargs):
        raise NotImplementedError("Parsing is not supported for this format")

    @classmethod
    def guess_format(self, text):
        return None

class SSAEvent(object):
    def __init__(self):
        self.start = 0 #: Start time (in milliseconds).
        self.end = 10000 #: End time (in milliseconds).
        self.text = "" #: Text (with SubStation override tags).
        self.style = "Default" #: Style name.
        self.type = "Dialogue"

    @property
    def duration(self):
        return self.end - self.start

    @property
    def is_comment(self):
        return self.type == "Comment"

    @is_comment.setter
    def is_comment(self, value):
        if value:
            self.type = "Comment"
        else:
            self.type = "Dialogue"

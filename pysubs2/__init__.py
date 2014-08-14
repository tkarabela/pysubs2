from .ssafile import SSAFile
from .ssaevent import SSAEvent
from .ssastyle import SSAStyle
from . import time, formats
from .exceptions import *
from .common import Color

#: Alias for :meth:`SSAFile.load()`.
load = SSAFile.load

#: Alias for :meth:`pysubs2.time.make_time()`.
make_time = time.make_time

#: Version of the pysubs2 library.
VERSION = "0.2.0-prealpha"

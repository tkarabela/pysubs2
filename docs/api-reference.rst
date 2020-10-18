API Reference
=============

.. note:: The documentation is written from Python 3 point of view; a "string" means Unicode string.

Supported input/output formats
------------------------------

pysubs2 is built around *SubStation Alpha*, the native subtitle format of `Aegisub <http://www.aegisub.org/>`_.
This format is popular in anime fansub community as it allows for rich text formatting and even animations
and vector graphics.

**SubStation Alpha** --- supported in two versions:

- .ass files (Advanced SubStation Alpha v4.0+), format identifier is ``"ass"``.
- .ssa files (SubStation Alpha v4.0), format identifier is ``"ssa"``.

**SubRip** --- .srt files, format identifier is ``"srt"``. Widely used subtitle format, it uses HTML
tags for formatting, though it is usually not heavily formatted (as opposed to *SubStation*).

**MicroDVD** --- .sub files, format identifier is ``"microdvd"``. This format uses frames to describe start/end times,
instead of hour/minute/second, which means it is dependent on framerate of the video. For proper retiming and conversion,
you need to know the framerate (sometimes it is given in the first subtitle, which ``pysubs2`` will autodetect and use).

**MPL2** --- Time-based format similar to MicroDVD, format identifier is ``"mpl2"``. To save subtitles in MPL2 format,
use ``subs.save("subtitles.txt", format_="mpl2")``.

**TMP** --- Time-based format, format identifier is ``"tmp"``. A very simple format which only specifies starting time
for each subtitle, eg. ``0:00:13:This is a subtitle``. Subtitle length is calculated automatically based on character
count. This older subtitle format is also referred to as "TMP Player" format.

**WebVTT** --- Time-based format similar to SubRip, format identifier is ``"vtt"``. Currently implemented
as a flavour of SubRip, with no extra support for WebVTT-specific features like styles or subtitle alignment.
`Link to WebVTT specification <https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API>`_, official name is
"Web Video Text Tracks Format".

**JSON**-serialized internal representation, which amounts to ASS. Format identifier is ``"json"``.

``pysubs2`` --- the main module
-------------------------------

.. automodule:: pysubs2
   :members: load, make_time, Color, VERSION

``SSAFile`` --- a subtitle file
-------------------------------

.. autoclass:: pysubs2.SSAFile
   :members: events, styles, info, fps, format, aegisub_project

Reading and writing subtitles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using path to file
++++++++++++++++++

.. automethod:: SSAFile.load
.. automethod:: SSAFile.save

Using string
++++++++++++

.. automethod:: SSAFile.from_string
.. automethod:: SSAFile.to_string

Using file object
+++++++++++++++++

.. automethod:: SSAFile.from_file
.. automethod:: SSAFile.to_file

Retiming subtitles
~~~~~~~~~~~~~~~~~~

.. automethod:: SSAFile.shift
.. automethod:: SSAFile.transform_framerate

Working with styles
~~~~~~~~~~~~~~~~~~~

.. automethod:: SSAFile.rename_style
.. automethod:: SSAFile.import_styles

Misc methods
~~~~~~~~~~~~

.. automethod:: SSAFile.equals
.. automethod:: SSAFile.sort


``SSAEvent`` --- one subtitle
-----------------------------

.. autoclass:: pysubs2.SSAEvent
   :members:

``SSAStyle`` --- a subtitle style
---------------------------------

.. autoclass:: pysubs2.SSAStyle
   :members:

``pysubs2.time`` --- time-related utilities
-------------------------------------------

.. automodule:: pysubs2.time
   :members:
   :exclude-members: Times

``pysubs2.exceptions`` --- thrown exceptions
--------------------------------------------

.. automodule:: pysubs2.exceptions
   :members:

``pysubs2.formats`` --- subtitle format implementations
-------------------------------------------------------

.. note:: This submodule contains pysubs2 internals. It's mostly of interest if you're looking to implement a subtitle format not supported by the library. In that case, have a look at :class:`pysubs2.formats.FormatBase`.

.. autofunction:: pysubs2.substation.parse_tags

.. automodule:: pysubs2.formats
   :members:

.. autoclass:: pysubs2.formats.FormatBase
   :members:

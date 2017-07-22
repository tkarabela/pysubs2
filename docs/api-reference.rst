API Reference
=============

.. note:: The documentation is written from Python 3 point of view; a "string" means Unicode string.

Supported input/output formats
------------------------------

pysubs2 is built around *SubStation Alpha*, the native subtitle format of `Aegisub <http://www.aegisub.org/>`_.

**SubStation Alpha** --- supported in two versions:

- .ass files (Advanced SubStation Alpha v4.0+), format identifier is ``"ass"``.
- .ssa files (SubStation Alpha v4.0), format identifier is ``"ssa"``.

**SubRip** --- .srt files, format identifier is ``"srt"``.

**MicroDVD** --- .sub files, format identifier is ``"microdvd"``.

**MPL2** --- .txt files, format identifier is ``"mpl2"``. Time-based format similar to MicroDVD.

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

.. autofunction:: pysubs2.formats.substation.parse_tags

.. automodule:: pysubs2.formats
   :members:

.. autoclass:: pysubs2.formats.FormatBase
   :members:

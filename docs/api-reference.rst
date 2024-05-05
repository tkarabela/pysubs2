API Reference
=============

``pysubs2`` --- the main module
-------------------------------

.. automodule:: pysubs2
   :members: load, load_from_whisper, make_time, Color, VERSION

.. autoenum:: pysubs2.Alignment

``SSAFile`` --- a subtitle file
-------------------------------

.. autoclass:: pysubs2.SSAFile
   :members: events, styles, info, fps, format, aegisub_project, fonts_opaque

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

.. automethod:: SSAFile.remove_miscellaneous_events
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
   :show-inheritance:

``pysubs2.formats`` --- subtitle format implementations
-------------------------------------------------------

.. note:: This subpackage contains pysubs2 internals. It's mostly of interest if you're looking to implement
          a subtitle format not supported by the library. In that case, have a look at :class:`pysubs2.formats.FormatBase`.

.. autofunction:: pysubs2.formats.substation.parse_tags

.. automodule:: pysubs2.formats
   :members:

Subtitle format API
~~~~~~~~~~~~~~~~~~~

.. autoclass:: pysubs2.formats.FormatBase
   :members:

.. _subtitle-format-implementations:

Subtitle format implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here you can find specific details regarding support of the individual subtitle formats.

.. tip::
   Some formats support additional keyword parameters in their ``from_file()`` or ``to_file()`` methods.
   These are used to customize the parser/writer behaviour.


.. autoclass:: pysubs2.formats.substation.SubstationFormat
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.subrip.SubripFormat
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.mpl2.MPL2Format
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.tmp.TmpFormat
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.webvtt.WebVTTFormat
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.microdvd.MicroDVDFormat
   :members:
   :show-inheritance:

.. autoclass:: pysubs2.formats.jsonformat.JSONFormat
   :members:
   :show-inheritance:

Misc functions
--------------

.. autofunction:: pysubs2.whisper.load_from_whisper

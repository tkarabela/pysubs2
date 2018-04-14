pysubs2
=======

.. image:: https://travis-ci.org/tkarabela/pysubs2.svg?branch=master
    :target: https://travis-ci.org/tkarabela/pysubs2

pysubs2 is a Python library for editing subtitle files.
It’s based on *SubStation Alpha*, the native format of
`Aegisub <http://www.aegisub.org/>`_; it also supports *SubRip*,
*MicroDVD* and *MPL2* formats. There is a small CLI tool for batch conversion and retiming.

.. code:: bash

    $ pip install pysubs2
    $ pysubs2 --shift 0.3s *.srt
    $ pysubs2 --to srt *.ass

.. code:: python

    import pysubs2
    subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
    subs.shift(s=2.5)
    for line in subs:
        line.text = "{\\be1}" + line.text
    subs.save("my_subtitles_edited.ass")

To learn more, please `see the documentation <http://pysubs2.readthedocs.io>`_.

pysubs2 is licensed under the MIT license (see LICENSE.txt).

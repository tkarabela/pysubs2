pysubs2
=======

.. image:: https://travis-ci.org/tkarabela/pysubs2.svg?branch=master
    :target: https://travis-ci.org/tkarabela/pysubs2

pysubs2 is a Python library for editing subtitle files.
It’s based on *SubStation Alpha*, the native format of
`Aegisub <http://www.aegisub.org/>`_; it also supports *SubRip* and
*MicroDVD* formats. There is a small CLI tool for batch conversion and retiming.

.. code:: bash

    $ python -m pysubs2 --shift 0.3s *.srt
    $ python -m pysubs2 --to srt *.ass

.. code:: python

    import pysubs2
    subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
    subs.shift(s=2.5)
    for line in subs:
        line.text = "{\\be1}" + line.text
    subs.save("my_subtitles_edited.ass")

To learn more, please `see the documentation <http://pythonhosted.org/pysubs2>`_.

pysubs2 is licensed under the MIT license (see LICENSE.txt).

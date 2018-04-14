Using pysubs2 from the Command Line
===================================

Do you want to convert subtitle files from one format to another, or do simple retiming?
You can use pysubs2 CLI, which is accessible through the ``pysubs2`` command installed
along with the library. Alternatively, the CLI can also be invoked by executing the pysubs2 module:
``python -m pysubs2``.

See ``pysubs2 --help`` for usage. Here are some examples::

    pysubs2 --to srt *.ass
    pysubs2 --to microdvd --fps 23.976 *.ass
    pysubs2 --shift 0.3s *.srt
    pysubs2 --shift 0.3s <my_file.srt >retimed_file.srt
    pysubs2 --shift-back 0.3s --output-dir retimed *.srt
    pysubs2 --transform-framerate 25 23.976 *.srt

.. warning::
    
    By default, the script works in-place; original files are overwritten. You can use the ``-o/--output-dir``
    option to specify output directory or process files in UNIX pipe fashion (``pysubs2 <infile >outfile``).

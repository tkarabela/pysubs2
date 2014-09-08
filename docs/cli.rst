Using pysubs2 from the Command Line
===================================

Do you want to convert subtitle files from one format to another, or do simple retiming? You can use pysubs2 CLI.

There are two ways to use the CLI:

1. Using the ``pysubs2.py`` script which should have been installed on your system along with pysubs2, or
2. by executing the pysubs2 module: ``python -m pysubs``.

See ``pysubs2.py --help`` for usage. Here are some examples::

    pysubs2.py --to srt *.ass
    pysubs2.py --to microdvd --fps 23.976 *.ass
    pysubs2.py --shift 0.3s *.srt
    pysubs2.py --shift 0.3s <my_file.srt >retimed_file.srt
    pysubs2.py --shift-back 0.3s --output-dir retimed *.srt
    pysubs2.py --transform-framerate 25 23.976 *.srt

.. warning::
    
    By default, the script works in-place; original files are overwritten. You can use the ``-o/--output-dir`` option to specify output directory or process files in single-file mode (``pysubs2.py <infile >outfile``).

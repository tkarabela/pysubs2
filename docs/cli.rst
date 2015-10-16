Using pysubs2 from the Command Line
===================================

Do you want to convert subtitle files from one format to another, or do simple retiming? You can use pysubs2 CLI, which is invoked by executing the pysubs2 module: ``python -m pysubs2``.

See ``python -m pysubs2 --help`` for usage. Here are some examples::

    python -m pysubs2 --to srt *.ass
    python -m pysubs2 --to microdvd --fps 23.976 *.ass
    python -m pysubs2 --shift 0.3s *.srt
    python -m pysubs2 --shift 0.3s <my_file.srt >retimed_file.srt
    python -m pysubs2 --shift-back 0.3s --output-dir retimed *.srt
    python -m pysubs2 --transform-framerate 25 23.976 *.srt

.. warning::
    
    By default, the script works in-place; original files are overwritten. You can use the ``-o/--output-dir`` option to specify output directory or process files in single-file mode (``python -m pysubs2 <infile >outfile``).

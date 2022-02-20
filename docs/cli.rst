Using pysubs2 from the Command Line
===================================

Do you want to convert subtitle files from one format to another, or do simple retiming?
You can use pysubs2 CLI, which is accessible through the ``pysubs2`` command installed
along with the library. Alternatively, the CLI can also be invoked by executing the pysubs2 module:
``python -m pysubs2``.

See ``pysubs2 --help`` for usage. Here are some examples::

    pysubs2 --to srt *.ass
    pysubs2 --to srt --clean *.ass
    pysubs2 --to microdvd --fps 23.976 *.ass
    pysubs2 --shift 0.3s *.srt
    pysubs2 --shift 0.3s <my_file.srt >retimed_file.srt
    pysubs2 --shift-back 0.3s --output-dir retimed *.srt
    pysubs2 --transform-framerate 25 23.976 *.srt

For formats other than SubStation, comment and drawing lines will be skipped. If you'd like a bit more
aggressive skipping, try the ``--clean`` option, which will also try to skip karaoke and duplicated lines.

.. warning::
    
    By default, the script works in-place; original files are overwritten. You can use the ``-o/--output-dir``
    option to specify output directory or process files in UNIX pipe fashion (``pysubs2 <infile >outfile``).

CLI parameters
--------------

.. use program-output directive here when we figure out how to make it work on readthedocs

::

    usage: pysubs2 [-h] [-v] [-f {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}] [-t {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}] [--input-enc ENCODING] [--output-enc ENCODING] [--fps FPS] [-o DIR] [--clean] [--verbose]
                   [--shift TIME | --shift-back TIME | --transform-framerate FPS1 FPS2] [--srt-keep-unknown-html-tags] [--srt-keep-ssa-tags] [--sub-no-write-fps-declaration]
                   [FILE [FILE ...]]

    The pysubs2 CLI for processing subtitle files.
    https://github.com/tkarabela/pysubs2

    positional arguments:
      FILE                  Input subtitle files. Can be in SubStation Alpha (*.ass, *.ssa), SubRip (*.srt), MicroDVD (*.sub) or other supported format. When no files are specified, pysubs2 will work as a pipe, reading from
                            standard input and writing to standard output.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -f {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}, --from {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}
                            By default, subtitle format is detected from the file. This option can be used to skip autodetection and force specific format. Generally, it should never be needed.
      -t {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}, --to {srt,ass,ssa,microdvd,json,mpl2,tmp,vtt}
                            Convert subtitle files to given format. By default, each file is saved in its original format.
      --input-enc ENCODING  Character encoding for input files. By default, UTF-8 is used for both input and output.
      --output-enc ENCODING
                            Character encoding for output files. By default, it is the same as input encoding. If you wish to convert between encodings, make sure --input-enc is set correctly! Otherwise, your output files will
                            probably be corrupted. It's a good idea to back up your files or use the -o option.
      --fps FPS             This argument specifies framerate for MicroDVD files. By default, framerate is detected from the file. Use this when framerate specification is missing or to force different framerate.
      -o DIR, --output-dir DIR
                            Use this to save all files to given directory. By default, every file is saved to its parent directory, ie. unless it's being saved in different subtitle format (and thus with different file
                            extension), it overwrites the original file.
      --clean               Attempt to remove non-essential subtitles (eg. karaoke, SSA drawing tags), strip styling information when saving to non-SSA formats
      --verbose             Print misc logging
      --shift TIME          Delay all subtitles by given time amount. Time is specified like this: '1m30s', '0.5s', ...
      --shift-back TIME     The opposite of --shift (subtitles will appear sooner).
      --transform-framerate FPS1 FPS2
                            Multiply all timestamps by FPS1/FPS2 ratio.

    optional arguments (SRT):
      --srt-keep-unknown-html-tags
      --srt-keep-ssa-tags

    optional arguments (MicroDVD):
      --sub-no-write-fps-declaration

    usage examples:
      python -m pysubs2 --to srt *.ass
      python -m pysubs2 --to srt --clean *.ass
      python -m pysubs2 --to microdvd --fps 23.976 *.ass
      python -m pysubs2 --shift 0.3s *.srt
      python -m pysubs2 --shift 0.3s <my_file.srt >retimed_file.srt
      python -m pysubs2 --shift-back 0.3s --output-dir retimed *.srt
      python -m pysubs2 --transform-framerate 25 23.976 *.srt

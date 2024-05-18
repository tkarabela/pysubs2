API tutorial: Let's ``import pysubs2``
======================================

This tutorial will show you how to use most of what pysubs2 library has to offer. If you are familiar with Python and Aegisub, you will hopefully find the API quite intuitive.

If you want to follow along in your REPL, make sure to have Python 3 and pysubs2 installed.

Reading subtitle file
---------------------

Let's settle on a simple subtitle file first.

    >>> SIMPLE_FILE = """\
    ... 1
    ... 00:00:00,000 --> 00:01:00,000
    ... Once upon a time,
    ... 
    ... 2
    ... 00:01:00,000 --> 00:02:00,000
    ... there was a SubRip file
    ... with two subtitles.
    ... """
    >>> with open("subtitles.srt", "w") as fp:
    ...      fp.write(SIMPLE_FILE)

Now that we have a real file on the harddrive, let's import pysubs2 and load it.

    >>> import pysubs2
    >>> subs = pysubs2.load("subtitles.srt")
    >>> subs
    <SSAFile with 2 events and 1 styles, last timestamp 0:02:00>

Now we have a subtitle file, the :class:`pysubs2.SSAFile` object. It has two "events", ie. subtitles. You can treat ``subs`` as a list:

    >>> subs[0].text
    "Once upon a time,"
    >>> for line in subs:
    ...     print(line.text)
    Once upon a time,
    there was a SubRip file\\Nwith two subtitles.

Individual subtitles are :class:`pysubs2.SSAEvent` objects and have the attributes you'd expect, like ``start``, ``end`` and ``text``. Notice that the second subtitle text doesn't contain a newline, but literal "backlash N", which is how SubStation represents newlines. There could also be override tags like ``{\i1}`` for italics.

.. tip::
   If you don't entertain SubStation, there is also a :attr:`pysubs2.SSAEvent.plaintext` property which hides override tags
   and translates newlines for you. Be warned, however, that writing to this property throws away any override tags.

    >>> for line in subs:
    ...     print(line.plaintext)
    Once upon a time,
    there was a SubRip file
    with two subtitles.

A point about character encoding
################################

By default, pysubs2 uses `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`_ character encoding when reading and writing files,
which enjoys wide software support, can represent any character from `Unicode <https://en.wikipedia.org/wiki/Unicode>`_,
and is efficient in terms of disk space. It's arguably "the" character encoding to use for text storage today, but it
hasn't always been like this, and it's possible that the subtitle files you will be dealing with use some other
encoding.

UTF-8 is a superset of `ASCII <https://en.wikipedia.org/wiki/ASCII>`_ and it's defined in such a way that files using
other encodings are very unlikely to form valid UTF-8 file. In other words, if your non-UTF-8 file contains characters
such as accented Latin letters, East Asian scripts, etc., instead of question marks or wrong characters in the output,
you will get an error like this:

    >>> import pysubs2
    >>> subs = pysubs2.load("subtitles.srt")
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf8 in position 110: invalid start byte

When this happens, you have two options:

    1. **If you need to work with subtitle text (eg. for translation)**, you must specify the correct encoding using the ``encoding``
       parameter for :meth:`pysubs2.load()`,
       eg. ``pysubs2.load("subtitles.srt", encoding="latin-1")``. If you don't know which encoding
       to use, you can try autodetecting it using a library like `charset-normalizer <https://pypi.org/project/charset-normalizer/>`_
       or `chardet <https://pypi.org/project/chardet/>`_.
    2. **If you don't need to read/modify subtitle text (eg. for retiming or format conversion)**, you can try using
       ``errors="surrogateescape"`` to wrap non-UTF-8 characters as `Unicode surrogate pairs <https://en.wikipedia.org/wiki/Universal_Character_Set_characters#Surrogates>`_
       and effectively pass them through to output, eg. ``pysubs2.load("subtitles.srt", errors="surrogateescape")``.
       This will only work if the actual character encoding is sufficiently "ASCII-like"
       that pysubs2 recognizes the file structure, which may fail with multi-byte encodings. The CLI tool uses this
       by default for better user experience.

Lastly, there have been reports about rare subtitle files with mixed character encodings. If you have the misfortune
to stumble upon such a file, use ``errors="surrogateescape"`` which will allow you to get the input ``bytes`` of a particular
subtitle by using: ``subs[0].text.encode("utf-8", "surrogateescape")``. You can then set the :attr:`pysubs2.SSAEvent.text`
to whatever is the correct decoded text.

Working with timing
-------------------

Let's have a look at the timestamps.

    >>> subs[1].start
    60000

That is 60,000 milliseconds, or one minute. pysubs2 uses plain :class:`int` milliseconds for time. Since you probably don't want to convert all times to milliseconds by hand, there is a handy function called :func:`pysubs2.make_time()`. You can use this function to give times in minutes and seconds, but also in frames.

    >>> subs[1].start == pysubs2.make_time(s=2)
    True
    >>> subs[1].start == pysubs2.make_time(frames=50, fps=25)
    True

.. tip:: :class:`pysubs2.SSAEvent` objects define ordering with respect to time, meaning you can sort them chronologically. There is :meth:`pysubs2.SSAFile.sort()` method for this purpose.

Let's write a function to retime a subtitle file by adding a constant to all timestamps!

    >>> def shift(subs, ms):
    ...     for line in subs:
    ...         line.start += ms
    ...         line.end += ms
    shift(subs, 500)

Well, it turns out the library can already do this with :meth:`pysubs2.SSAFile.shift()`, which takes the same arguments as :func:`pysubs2.make_time()`. Let's shift the subtitles back.

    >>> subs.shift(s=-0.5)

.. note:: You can have negative timestamps in your ``subs``. They are assumed to be zero for purposes of export.

Working with styles
-------------------

As you've seen already with the newlines, pysubs2 works with SubStation, meaning our SRT file actually has a "Default" style associated with its subtitles.

    >>> subs.styles["Default"]
    <SSAStyle 20.0px 'Arial'>

Let's add one more style, with italics, and let the second subtitle have it.

    >>> my_style = subs.styles["Default"].copy()
    >>> my_style.italic = True
    >>> subs.styles["MyStyle"] = my_style
    >>> subs[1].style = "MyStyle"

Notice that the subtitle object (:class:`pysubs2.SSAEvent`) and the style object (:class:`pysubs2.SSAStyle`) aren't really connected. Instead, styles are referred to by their name in the :attr:`pysubs2.SSAFile.styles` dictionary.

You can also create a :class:`pysubs2.SSAStyle` directly, specifying the attributes you want, while the other attributes will use values from the default style:

    >>> top_style = pysubs2.SSAStyle(fontsize=10, alignment=pysubs2.Alignment.TOP_CENTER)
    >>> subs.styles["Top"] = my_style
    >>> subs[1].style = "Top"

.. tip:: Renaming a style is a little difficult, because you also have to fix all references to the old name. The :meth:`pysubs2.SSAFile.rename_style()` method does what's needed behind the scenes.

Saving subtitle file
--------------------

Now that the second subtitle uses "MyStyle", it should appear in italics. Let's export to SRT again to see if that's the case!

::

    >>> modified_srt = subs.to_string("srt")
    >>> modified_srt
    """\
    1
    00:00:00,000 --> 00:01:00,000
    Once upon a time,
    
    2
    00:01:00,000 --> 00:02:00,000
    <i>there was a SubRip file
    with two subtitles.</i>
    
    """

Indeed it is. Of course, since SubRip has no concept of styles, the italics will get converted to inline tags and styles will be lost if we load this exported file:

    >>> modified_subs = pysubs2.SSAFile.from_string(modified_srt)
    >>> modified_subs[1].text
    "{\\i1}there was a SubRip file\\Nwith two subtitles.{\\i0}"
    >>> modified_subs[1].style
    "Default"

It's better to save the file as ASS so that style information isn't lost.

::

    >>> subs.save("modified_subtitles.ass")
    >>> with open("modified_subtitles.ass") as fp:
    ...      print(fp.read())
    [Script Info]
    ; Script generated by pysubs2
    ; https://pypi.python.org/pypi/pysubs2
    WrapStyle: 0
    ScaledBorderAndShadow: yes
    Collisions: Normal
    ScriptType: v4.00+

    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    Style: Default,Arial,20.0,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100.0,100.0,0.0,0.0,1,2.0,2.0,2,10,10,10,1
    Style: MyStyle,Arial,20.0,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,-1,0,0,100.0,100.0,0.0,0.0,1,2.0,2.0,2,10,10,10,1

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    Dialogue: 0,0:00:00.00,0:01:00.00,Default,,0,0,0,,Once upon a time,
    Dialogue: 0,0:01:00.00,0:02:00.00,MyStyle,,0,0,0,,there was a SubRip file\Nwith two subtitles.

Example: Creating top/bottom bilingual subtitles
------------------------------------------------

Let's say you have English and Italian subtitles for the same movie and you wish to create combined subtitle file with Italian subtitles located at the bottom and English at the top, with different colors
for each language. The following code creates this combined file and saves it in SubStation Alpha format (this is important, you need to use a format that supports positioning):

::

    import pysubs2
    from pysubs2 import Alignment, Color, SSAFile, SSAStyle

    subs_en = pysubs2.load("subs.en.srt")  # read input subtitles in SRT format
    subs_it = pysubs2.load("subs.it.srt")

    subs = SSAFile()
    subs.styles = {
        "bottom": SSAStyle(alignment=Alignment.BOTTOM_CENTER, primarycolor=Color(255, 255, 0)),
        "top": SSAStyle(alignment=Alignment.TOP_CENTER, primarycolor=pysubs2.Color(0, 128, 128)),
    }
    for e in subs_it:
        e.style = "bottom"
        subs.append(e)
    for e in subs_en:
        e.style = "top"
        subs.append(e)

    subs.save("subs.ass")  # write subtitles in ASS format (supports formatting)

And that's it! Now you should be a little familiar with pysubs2. Have a look at the API Reference to see what's there.

Some final thoughts, in no particular order:

- The library tries its best to read given file. Format detection and actual parsing is rather benevolent.
- Only basic SubRip/MicroDVD tags are supported.
- If you are unsure about SubStation, get familiar with the `Aegisub subtitle editor <http://www.aegisub.org/>`_. You can also use `the SubStation specification <http://moodub.free.fr/video/ass-specs.doc>`_ for reference.
- When working with MicroDVD, you sometimes have to specify the ``fps`` argument when loading and saving. There is a convention to specify framerate in the first subtitle, which pysubs2 handles transparently.
- If your goal is to create complex effects with frame-perfect timing, you may want to check out the `PyonFX <https://github.com/CoffeeStraw/PyonFX>`_ library which is focused on this use case. `This discussion of timestamps vs. frames <https://github.com/tkarabela/pysubs2/issues/57>`_ may also be relevant to you.

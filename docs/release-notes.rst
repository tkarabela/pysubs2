Release Notes
=============

**1.7.1** --- released on 2024-05-19

- Fixed missing ``pysubs2.formats`` subpackage in PyPI distributions (Issue #92)
- Test sdist and wheel distributions in CI

**1.7.0** --- released on 2024-05-19 (yanked)

- Added ``errors`` option for :meth:`pysubs2.load()`, :meth:`pysubs2.SSAFile.save()` and related methods, exposing
  the encoding handling option of builtin function ``open()``. By default, this option uses value ``None`` which
  is consistent with behaviour of previous versions of the library. However, it's possible to use ``"surrogateescape"``
  to bypass the need to specify correct character encoding in some cases (see the tutorial). In the CLI, surrogateescape
  is now the default behaviour.
- SubStation writer now correctly handles timestamps which are not rounded to centiseconds, for example
  ``00:36:48,998`` from a SRT file no longer produces the invalid ASS timestamp ``0:36:48.100`` (Issue #83),
  patch by moi15moi (https://github.com/moi15moi)
- MicroDVD parser now only uses FPS declaration from the first subtitle if the line starts with ``{1}{1}``,
  matching VLC Player behaviour; the old behaviour is available under the ``strict_fps_inference`` reader option
  (Issue #71)
- SubStation writer now omits fractional part for numeric values if it is zero, patch by Andrey Efremov (https://github.com/PalmtopTiger)
- CLI now shows help message when called without arguments (Issue #81), patches by Northurland (https://github.com/Northurland) and Andrey Efremov (https://github.com/PalmtopTiger)
- pysubs2 now raises correct exception (:class:`pysubs2.exceptions.FormatAutodetectionError`) when attempting to read
  a JSON file that was not saved by pysubs2 (Issue #85)
- More robust SubStation parser (Issues #87, #89)
- Added test data to source distribution (Issue #75)
- Code now passes MyPy check in strict mode, as well as Ruff check
- Added support for Python 3.12, removed support for Python 3.7


**1.6.1** --- released on 2023-04-02

- WebVTT now correctly writes events in cue start order, patch by Anton Melser (https://github.com/AntonOfTheWoods)
- Improved type hints
- Minor documentation fixes and improvements
- Migrated CI from CircleCI to GitHub, added Codecov to CI (we're currently at 93% test coverage)

**1.6.0** --- released on 2022-11-28

- Basic support for ``[Graphics]`` in SubStation files (Issue #59)
- SubStation now outputs timestamps with properly rounded centiseconds, instead of always rounding down (Issue #57)
- ``SSAStyle.alignment`` now uses new ``pysubs2.Alignment`` enum type instead of ``int`` (eg. ``Alignment.TOP_CENTER`` instead of ``8``). Support for integers is retained.
- The library will now issue ``RuntimeWarning`` when saving a timestamp that is too large to be represented in given format (it will be clamped to its maximum legal value).

**1.5.0** --- released on 2022-11-15

- Added support for loading `OpenAI Whisper <https://github.com/openai/whisper>`_ transcription output: ``result = model.transcribe(...); subs = pysubs2.load_from_whisper(result)`` (issue #58)
- Removed old-style ``setup.py``, moved to declarative ``setup.cfg`` and ``pyproject.toml``

**1.4.4** --- released on 2022-11-01

- Added support for Python 3.11 (issue #56)

**1.4.3** --- released on 2022-08-19

- Added support for SubStation files with ``H:M:S.cs`` timestamps, patch by Florian Badie (https://github.com/odrling)

**1.4.2** --- released on 2022-04-08

- Added support for SubStation files with ``H:MM:SS`` timestamps (issue #50)
- Migrated CI from Travis to CircleCI, added Mypy typecheck to CI

**1.4.1** --- released on 2022-03-02

- Added option to keep all HTML tags in SRT input: ``pysubs2.load("subs.srt", keep_html_tags=True)`` (Issue #48)
- Added support for ``<b>`` tags in SRT parser

**1.4.0** --- released on 2022-02-20

- Added option to keep SubStation override tags in SRT output: ``subs.to_file("subs.srt", keep_ssa_tags=True)`` (Issue #48)
- Added format-specific extra options to CLI: ``--srt-keep-unknown-html-tags``, ``--srt-keep-ssa-tags``, ``--sub-no-write-fps-declaration``

**1.3.1** --- released on 2021-12-19

- Fixed WebVTT timestamps output, patch by Mathias Köhler (https://github.com/interru)
- Added slice indexing support to ``SSAFile``
- pysubs2 now passes MyPy non-strict typecheck (with MyPy 0.920)

**1.3.0** --- released on 2021-10-02

- More robust SubStation parser (Issue #45)
- Added Python 3.10 support, patch by luk1337 (https://github.com/luk1337)
- Migrated tests from nose to pytest

**1.2.0** --- released on 2021-05-08

- Basic support for ``[Fonts]`` in SubStation files (Issue #41)
- Default file encoding for CLI is now UTF-8, bringing it in line with how the Python API works (Issue #38)
- The ``--clean`` option for CLI now skips styling when writing non-SubStation formats (Issue #39)
- ``SSAEvent``, ``SSAStyle`` and ``Color`` are now dataclasses
- Improved Sphinx documentation (documented format implementation classes, including what extra read/write
  keyword parameters they support; included CLI ``--help`` output for parameter reference)

**1.1.0** --- released on 2021-02-27

- Added ``--clean`` option to CLI for more aggressive skipping of unwanted subtitles (Issue #37)

**1.0.0** --- released on 2020-10-19

- Dropped support for Python 2. The library now requires Python 3.7 or newer.
- Added type hints and also explicit keyword arguments to ``SSAEvent``, ``SSAStyle``, which should improve coding experience.
- Support for WebVTT subtitle format (this used to be somewhat possible using the SRT parser, but support is much better now)
- Lines with ASS drawing tags (eg. ``{\p1}``) are not written to non-SubStation files, patch by pannal (https://github.com/pannal)
- ASS-style hex colors are supported in SSA files, patch by Mike Wang (https://github.com/MikeWang000000)
- TMP reader no longer creates subtitles with overlapping times (Issue #35)

**0.2.4** --- released on 2019-06-23

- Support for TMP subtitle format, patch by bkiziuk (https://github.com/bkiziuk)
- Support for Python 3.7 thanks to cleaning up string escape issues,
  patch by Spencer Berger (https://github.com/bergerspencer)
- Added ``keep_unknown_html_tags`` parser option for passing through HTML tags in SubRip files (Issue #26)
- SubStation files with negative timestamps no longer break the parser (Issue #28)
- SubStation files with no whitespace in info sections are handled correctly (Issue #14),
  patch by Joshua Avalon (https://github.com/joshuaavalon)
- Updated badges in GitHub readme, patch by Eray Erdin (https://github.com/erayerdin)

**0.2.3** --- released on 2018-04-14

- Added a CLI script ``pysubs2``, patch by Piotr Staroszczyk (https://github.com/oczkers)
- Loading a SRT file with empty subtitles behaves more correctly (Issue #11)
- Using the library from Python 2 is easier due to less pedantic ``str``/``unicode`` checks (Issue #12)

**0.2.2** --- released on 2017-07-22

- Support for MPL2 subtitle format, patch by pannal (https://github.com/pannal)
- Dropped support for Python 3.2

**0.2.1** --- released on 2015-10-17

- CLI can now be invoked by ``python -m pysubs2`` only; broken ``pysubs2.py`` script has been removed (Issue #1).
- Loading a SubStation file no longer swaps color channels (Issue #3).
- pysubs2 now preserves Aegisub 3.2+ project settings (the ``[Aegisub Project Garbage]`` section, stored in :attr:`pysubs2.SSAFile.aegisub_project` dict).
- SubStation version is now correctly declared in ``[Script Info]`` section as ``ScriptType`` (instead of ``ScriptInfo``).

**0.2.0** --- released on 2014-09-09

- Initial release.

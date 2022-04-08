Release Notes
=============

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

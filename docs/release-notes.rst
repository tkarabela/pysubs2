Release Notes
=============

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

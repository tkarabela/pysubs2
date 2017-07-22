Release Notes
=============

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

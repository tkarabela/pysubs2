#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from textwrap import dedent
from pysubs2 import VERSION

setup(
    name = "pysubs2",
    packages = ["pysubs2"],
    version = VERSION,
    author = "Tomas Karabela",
    author_email = "tkarabela@seznam.cz",
    url = "https://github.com/tkarabela/pysubs2",
    keywords = "SubStation SubRip MicroDVD ass srt sub subtitles",
    description = "A library for editing subtitle files",
    long_description = dedent(r"""\
        pysubs2 is a Python library for editing subtitle files.
        It’s based on *SubStation Alpha*, the native format of
        `Aegisub <http://www.aegisub.org/>`_; it also supports *SubRip (SRT)*,
        *MicroDVD*, *MPL2*, *TMP* and *WebVTT* formats. There is a small CLI tool for batch conversion
        and retiming.

        ::

            import pysubs2
            subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
            subs.shift(s=2.5)
            for line in subs:
                line.text = "{\\be1}" + line.text
            subs.save("my_subtitles_edited.ass")

        """),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Multimedia :: Video",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Typing :: Typed",
        ],
    entry_points={'console_scripts': ['pysubs2 = pysubs2.cli:__main__']},
    python_requires=">=3.7",
    )

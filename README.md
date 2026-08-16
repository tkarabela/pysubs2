[![pysubs2 build master branch](https://img.shields.io/github/actions/workflow/status/tkarabela/pysubs2/main.yml?branch=master)](https://github.com/tkarabela/pysubs2/actions)
[![pysubs2 test code coverage](https://img.shields.io/codecov/c/github/tkarabela/pysubs2)](https://app.codecov.io/github/tkarabela/pysubs2)
[![Static Badge](https://img.shields.io/badge/MyPy%20%26%20Pyrefly%20%26%20Ruff-checked-blue?style=flat)](https://github.com/tkarabela/pysubs2/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - Status](https://img.shields.io/pypi/status/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - License](https://img.shields.io/pypi/l/pysubs2.svg?style=flat)](LICENSE.txt)
[![GitHub Repo stars](https://img.shields.io/github/stars/tkarabela/pysubs2?style=flat&label=GitHub%20stars)](https://github.com/tkarabela/pysubs2)

pysubs2
=======

pysubs2 is a Python library for editing subtitle files. It’s based on *SubStation Alpha*,
the native format of [Aegisub](http://www.aegisub.org/); it also supports *SubRip (SRT)*,
*MicroDVD*, *MPL2*, *TMP*, *WebVTT*, *TTML* and *SAMI* formats and *OpenAI Whisper* captions.

Goal of this library is to provide practical, robust handling for subtitle files
found in the wild (with all their questionable syntax). Internally, everything is converted to
a representation based on *ASS*, which is relevant if you want to process formatting.
Support for production/broadcast subtitle formats (or subtitle features beyond what *ASS* can express)
is not really a goal of the library; however, please open an issue if you have a use-case
where using this library would make sense to you.

Based on code originally created in 2011, in development ever since.
Thanks to all users and contributors over the years!

---

Quick links: [Documentation](http://pysubs2.readthedocs.io) · [Issues](https://github.com/tkarabela/pysubs2/issues) · [Contributing](https://github.com/tkarabela/pysubs2/blob/master/CONTRIBUTING.md) · [Source code](https://github.com/tkarabela/pysubs2)

---

## Usage

For more information, please see the tutorial and API reference in the [Documentation](http://pysubs2.readthedocs.io).

```python
import pysubs2
subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
subs.shift(s=2.5)
for line in subs:
    line.text = "{\\be1}" + line.text
subs.save("my_subtitles_edited.ass")
```

There is also a small CLI tool for batch conversion and retiming.

```bash
pip install pysubs2
pysubs2 --shift 0.3s *.srt
pysubs2 --to srt *.ass
```

## Installation

Simply `uv add pysubs2` or `pip install pysubs2`.

The library itself is pure Python, with no additional dependencies.

## Contributing

If you'd like to contribute code to the library, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

pysubs2 is licensed under the MIT license (see [LICENSE.txt](LICENSE.txt)).

pysubs2
=======

[![pysubs2 build master branch](https://img.shields.io/github/actions/workflow/status/tkarabela/pysubs2/main.yml?branch=master)](https://github.com/tkarabela/pysubs2/actions)
[![pysubs2 test code coverage](https://img.shields.io/codecov/c/github/tkarabela/pysubs2)](https://app.codecov.io/github/tkarabela/pysubs2)
[![Static Badge](https://img.shields.io/badge/MyPy%20%26%20Ruffle-checked-blue?style=flat)](https://github.com/tkarabela/pysubs2/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - Status](https://img.shields.io/pypi/status/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysubs2.svg?style=flat)](https://pypi.org/project/pysubs2/)
[![PyPI - License](https://img.shields.io/pypi/l/pysubs2.svg?style=flat)](LICENSE.txt)
[![GitHub Repo stars](https://img.shields.io/github/stars/tkarabela/pysubs2?style=flat&label=GitHub%20stars)](https://github.com/tkarabela/pysubs2)


pysubs2 is a Python library for editing subtitle files.
It’s based on *SubStation Alpha*, the native format of
[Aegisub](http://www.aegisub.org/); it also supports *SubRip (SRT)*,
*MicroDVD*, *MPL2*, *TMP* and *WebVTT* formats and *OpenAI Whisper* captions.

There is a small CLI tool for batch conversion and retiming.

```bash
pip install pysubs2
pysubs2 --shift 0.3s *.srt
pysubs2 --to srt *.ass
```

```python
import pysubs2
subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
subs.shift(s=2.5)
for line in subs:
    line.text = "{\\be1}" + line.text
subs.save("my_subtitles_edited.ass")
```

To learn more, please [see the documentation](http://pysubs2.readthedocs.io).
If you'd like to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).

pysubs2 is licensed under the MIT license (see [LICENSE.txt](LICENSE.txt)).

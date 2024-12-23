"""
pysubs2.formats.ttml tests

"""

import pytest
import pysubs2
from pysubs2 import SSAFile, SSAEvent, SSAStyle
import os.path as op


def get_data_path(filename: str) -> str:
    return op.join(op.dirname(__file__), "..", "data", filename)


@pytest.mark.parametrize(
    "ttml_filename, ass_ref_filename",
    [
        ["ttml_example.ttml", "ttml_example.ass"],
        ["ttml_example2.ttml", "ttml_example2.ass"],
    ]
)
def test_example_parse(ttml_filename: str, ass_ref_filename: str) -> None:
    subs = pysubs2.load(get_data_path(ttml_filename))
    ass_text = subs.to_string("ass")
    print(ass_text)
    with open(get_data_path(ass_ref_filename)) as fp:
        ref_text = fp.read()
    assert ass_text.strip() == ref_text.strip()


TEST_SERIALIZE_REFERENCE = """
<tt xmlns="http://www.w3.org/ns/ttml" xmlns:tts="http://www.w3.org/ns/ttml#styling">
  <head>
    <styling>
      <style id="Default" tts:fontFamily="Arial" tts:fontWeight="normal" tts:fontStyle="normal" tts:color="#FFFFFF" />
      <style id="My Italic" tts:fontFamily="Comic Sans MS" tts:fontWeight="normal" tts:fontStyle="italic" tts:color="#FFFFFF" />
    </styling>
  </head>
  <body>
    <div>
      <p begin="00:00:01.000" end="00:00:02.000" style="Default">Newline test<br />Newline test<br />Hardspace test End of test</p>
      <p begin="00:00:02.000" end="00:00:03.000" style="Default">Regular text<span tts:fontStyle="italic">Now in italics</span>not anymore</p>
      <p begin="00:00:02.000" end="00:00:03.000" style="My Italic">Italic text<span tts:fontStyle="normal">Now in regular</span>Italic again</p>
      <p begin="00:00:03.000" end="00:00:04.000" style="Default" tts:fontFamily="Comic Sans MS">New font for whole line</p>
      <p begin="00:00:04.000" end="00:00:05.000" style="Default">New font for <span tts:fontFamily="Comic Sans MS">part of line only</span>
      </p>
    </div>
  </body>
</tt>
"""


def test_serialize():
    subs = SSAFile()
    italic_style = subs.styles["My Italic"] = SSAStyle.DEFAULT_STYLE.copy()
    italic_style.italic = True
    italic_style.fontname = "Comic Sans MS"

    subs.extend([
        SSAEvent(start=1000, end=2000, text=r"Newline test\nNewline test\NHardspace test\hEnd of test"),
        SSAEvent(start=2000, end=3000, text=r"Regular text{\i1}Now in italics{\i0}not anymore"),
        SSAEvent(start=2000, end=3000, style="My Italic", text=r"Italic text{\i0}Now in regular{\r}Italic again"),
        SSAEvent(start=3000, end=4000, text=r"{\fnComic Sans MS}New font for whole line"),
        SSAEvent(start=4000, end=5000, text=r"New font for {\fnComic Sans MS}part of line only"),
    ])

    assert subs.to_string("ttml").strip() == TEST_SERIALIZE_REFERENCE.strip()
